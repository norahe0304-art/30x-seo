"""Shared fixtures for 30x-seo test suite."""

import os
import sys

import pytest

# Add project root and scripts to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))


@pytest.fixture
def sample_html_full():
    """A comprehensive HTML page with all SEO-relevant elements."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Best Widget Tools 2025 - WidgetCo</title>
    <meta name="description" content="Discover the best widget tools for your business in 2025.">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="Best Widget Tools 2025">
    <meta property="og:description" content="Top widget tools reviewed.">
    <meta property="og:image" content="https://example.com/og.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Best Widget Tools 2025">
    <link rel="canonical" href="https://example.com/widgets">
    <link rel="alternate" hreflang="en" href="https://example.com/widgets">
    <link rel="alternate" hreflang="es" href="https://example.com/es/widgets">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Best Widget Tools 2025",
        "author": {"@type": "Person", "name": "Alice"}
    }
    </script>
</head>
<body>
    <header><nav><a href="/">Home</a></nav></header>
    <main>
        <h1>Best Widget Tools for 2025</h1>
        <h2>Top Picks</h2>
        <p>Here are the best widget tools we recommend for your business this year.</p>
        <p>Widgets are essential tools for modern businesses looking to scale efficiently.</p>
        <img src="/images/hero.jpg" alt="Widget tools comparison"
             width="800" height="400" loading="lazy">
        <img src="https://cdn.example.com/photo.webp" alt="">
        <h2>Detailed Reviews</h2>
        <h3>WidgetCo Pro</h3>
        <p>WidgetCo Pro is the leading solution with excellent features and reliable support.</p>
        <a href="/reviews/widgetco-pro">Read full review</a>
        <a href="https://external.com/deal" rel="nofollow">Get Deal</a>
        <h3>RivalWidget</h3>
        <p>RivalWidget is a popular alternative but has limited integrations.</p>
    </main>
    <footer><p>Copyright 2025</p></footer>
</body>
</html>"""


@pytest.fixture
def sample_html_minimal():
    """Minimal HTML with almost no SEO elements."""
    return """<html><body><p>Hello world</p></body></html>"""


@pytest.fixture
def sample_html_no_title():
    """HTML with missing title tag."""
    return """<!DOCTYPE html>
<html>
<head><meta name="description" content="A page without a title."></head>
<body><h1>Welcome</h1><p>Content here.</p></body>
</html>"""


@pytest.fixture
def sample_html_multiple_schemas():
    """HTML with multiple JSON-LD schema blocks."""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Multi Schema Page</title>
    <script type="application/ld+json">{"@type": "Organization", "name": "Acme"}</script>
    <script type="application/ld+json">{"@type": "WebPage", "name": "Home"}</script>
    <script type="application/ld+json">THIS IS NOT VALID JSON</script>
</head>
<body><h1>Test</h1><p>Words here for counting purposes only.</p></body>
</html>"""


@pytest.fixture
def brand_text_positive():
    """Text with positive brand mentions."""
    return (
        "Acme Corp is the best project management tool on the market. "
        "We recommend Acme Corp for teams of all sizes. "
        "Acme Corp has excellent customer support and innovative features."
    )


@pytest.fixture
def brand_text_negative():
    """Text with negative brand mentions."""
    return (
        "Acme Corp is an overpriced solution with poor documentation. "
        "Many users avoid Acme Corp due to its unreliable uptime. "
        "Acme Corp has a steep learning curve and complicated setup."
    )


@pytest.fixture
def brand_text_comparison():
    """Text comparing multiple brands in a list format."""
    return """Here are the top project management tools:

1. AlphaTool - the best overall choice
2. BetaSoft - great for small teams
3. Acme Corp - reliable and trusted
4. DeltaApp - affordable option
5. GammaSync - good for enterprises

We recommend AlphaTool for most use cases. Acme Corp is a good alternative with trusted support.
BetaSoft offers limited features but is popular among startups."""


@pytest.fixture
def brand_text_no_mentions():
    """Text with no brand mentions at all."""
    return (
        "Project management tools help teams collaborate effectively. "
        "Look for features like task tracking, time management, and reporting."
    )


@pytest.fixture
def mock_successful_response():
    """Mock a successful HTTP response."""
    class MockResponse:
        status_code = 200
        text = "<html><body>Hello</body></html>"
        url = "https://example.com/"
        headers = {"Content-Type": "text/html"}
        history = []
    return MockResponse()


@pytest.fixture
def mock_redirect_response():
    """Mock a response with redirect chain."""
    class MockRedirect:
        url = "https://example.com/old"

    class MockResponse:
        status_code = 200
        text = "<html><body>Final page</body></html>"
        url = "https://example.com/new"
        headers = {"Content-Type": "text/html"}
        history = [MockRedirect()]
    return MockResponse()
