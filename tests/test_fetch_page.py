"""Tests for scripts/fetch_page.py - URL fetching with SSRF prevention."""

from unittest.mock import MagicMock, patch

import requests
from fetch_page import fetch_page


class TestSSRFPrevention:
    """Ensure private/internal IPs are blocked."""

    @patch("fetch_page.socket.gethostbyname")
    def test_blocks_localhost(self, mock_dns):
        mock_dns.return_value = "127.0.0.1"
        result = fetch_page("http://localhost/admin")
        assert result["error"] is not None
        assert "private" in result["error"].lower() or "internal" in result["error"].lower()

    @patch("fetch_page.socket.gethostbyname")
    def test_blocks_private_10_network(self, mock_dns):
        mock_dns.return_value = "10.0.0.1"
        result = fetch_page("http://internal-server.com")
        assert result["error"] is not None
        assert "private" in result["error"].lower() or "internal" in result["error"].lower()

    @patch("fetch_page.socket.gethostbyname")
    def test_blocks_private_192_network(self, mock_dns):
        mock_dns.return_value = "192.168.1.1"
        result = fetch_page("http://router.local")
        assert result["error"] is not None
        assert "Blocked" in result["error"]

    @patch("fetch_page.socket.gethostbyname")
    def test_blocks_private_172_network(self, mock_dns):
        mock_dns.return_value = "172.16.0.1"
        result = fetch_page("http://intranet.example.com")
        assert result["error"] is not None
        assert "Blocked" in result["error"]

    @patch("fetch_page.socket.gethostbyname")
    def test_blocks_loopback_ipv4(self, mock_dns):
        mock_dns.return_value = "127.0.0.1"
        result = fetch_page("http://127.0.0.1:8080/secret")
        assert result["error"] is not None
        assert "Blocked" in result["error"]


class TestURLValidation:
    """Test URL scheme validation."""

    def test_rejects_ftp_scheme(self):
        result = fetch_page("ftp://example.com/file.txt")
        assert result["error"] is not None
        assert "Invalid URL scheme" in result["error"]

    def test_rejects_file_scheme(self):
        result = fetch_page("file:///etc/passwd")
        assert result["error"] is not None
        assert "Invalid URL scheme" in result["error"]

    def test_rejects_javascript_scheme(self):
        result = fetch_page("javascript:alert(1)")
        assert result["error"] is not None
        assert "Invalid URL scheme" in result["error"]

    @patch("fetch_page.socket.gethostbyname")
    @patch("fetch_page.requests.Session")
    def test_prepends_https_when_no_scheme(self, mock_session_cls, mock_dns):
        mock_dns.return_value = "93.184.216.34"
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        mock_response.url = "https://example.com"
        mock_response.headers = {}
        mock_response.history = []
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        result = fetch_page("example.com")
        assert result["error"] is None
        # The session.get should have been called with https://
        call_args = mock_session.get.call_args
        assert call_args[0][0].startswith("https://")


class TestRedirectTracking:
    """Test redirect chain tracking."""

    @patch("fetch_page.socket.gethostbyname")
    @patch("fetch_page.requests.Session")
    def test_tracks_redirect_chain(self, mock_session_cls, mock_dns):
        mock_dns.return_value = "93.184.216.34"

        mock_redirect_1 = MagicMock()
        mock_redirect_1.url = "http://example.com/old"
        mock_redirect_2 = MagicMock()
        mock_redirect_2.url = "https://example.com/old"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Final"
        mock_response.url = "https://example.com/new"
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.history = [mock_redirect_1, mock_redirect_2]

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        result = fetch_page("http://example.com/old")
        assert result["redirect_chain"] == [
            "http://example.com/old",
            "https://example.com/old",
        ]
        assert result["url"] == "https://example.com/new"
        assert result["status_code"] == 200

    @patch("fetch_page.socket.gethostbyname")
    @patch("fetch_page.requests.Session")
    def test_no_redirects_empty_chain(self, mock_session_cls, mock_dns):
        mock_dns.return_value = "93.184.216.34"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Direct"
        mock_response.url = "https://example.com"
        mock_response.headers = {}
        mock_response.history = []

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        result = fetch_page("https://example.com")
        assert result["redirect_chain"] == []


class TestTimeoutHandling:
    """Test timeout and error handling."""

    @patch("fetch_page.socket.gethostbyname")
    @patch("fetch_page.requests.Session")
    def test_timeout_returns_error(self, mock_session_cls, mock_dns):
        mock_dns.return_value = "93.184.216.34"
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.Timeout()
        mock_session_cls.return_value = mock_session

        result = fetch_page("https://slow-site.com", timeout=5)
        assert result["error"] is not None
        assert "timed out" in result["error"].lower()

    @patch("fetch_page.socket.gethostbyname")
    @patch("fetch_page.requests.Session")
    def test_too_many_redirects(self, mock_session_cls, mock_dns):
        mock_dns.return_value = "93.184.216.34"
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.TooManyRedirects()
        mock_session_cls.return_value = mock_session

        result = fetch_page("https://redirect-loop.com")
        assert result["error"] is not None
        assert "redirect" in result["error"].lower()

    @patch("fetch_page.socket.gethostbyname")
    @patch("fetch_page.requests.Session")
    def test_ssl_error(self, mock_session_cls, mock_dns):
        mock_dns.return_value = "93.184.216.34"
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.SSLError("cert verify failed")
        mock_session_cls.return_value = mock_session

        result = fetch_page("https://bad-cert.com")
        assert result["error"] is not None
        assert "ssl" in result["error"].lower()

    @patch("fetch_page.socket.gethostbyname")
    @patch("fetch_page.requests.Session")
    def test_connection_error(self, mock_session_cls, mock_dns):
        mock_dns.return_value = "93.184.216.34"
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.ConnectionError("refused")
        mock_session_cls.return_value = mock_session

        result = fetch_page("https://down-site.com")
        assert result["error"] is not None
        assert "connection" in result["error"].lower()

    @patch("fetch_page.socket.gethostbyname", side_effect=__import__('socket').gaierror("DNS fail"))
    @patch("fetch_page.requests.Session")
    def test_dns_failure_falls_through_to_requests(self, mock_session_cls, mock_dns):
        """DNS resolution failure in SSRF check should not block; requests handles it."""
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.ConnectionError("Name resolution failed")
        mock_session_cls.return_value = mock_session

        result = fetch_page("https://nonexistent.invalid")
        assert result["error"] is not None


class TestSuccessfulFetch:
    """Test successful fetches return correct structure."""

    @patch("fetch_page.socket.gethostbyname")
    @patch("fetch_page.requests.Session")
    def test_result_structure(self, mock_session_cls, mock_dns):
        mock_dns.return_value = "93.184.216.34"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>OK</html>"
        mock_response.url = "https://example.com"
        mock_response.headers = {"Content-Type": "text/html", "Server": "nginx"}
        mock_response.history = []

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        result = fetch_page("https://example.com")
        assert result["error"] is None
        assert result["status_code"] == 200
        assert result["content"] == "<html>OK</html>"
        assert result["url"] == "https://example.com"
        assert "Content-Type" in result["headers"]
