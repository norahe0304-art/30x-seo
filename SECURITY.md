# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.3.x | Yes |
| 1.2.x | Security patches only |
| < 1.2 | No |

## Reporting a Vulnerability

If you discover a security vulnerability in 30x-seo, please report it responsibly.

### How to Report

1. **Do NOT open a public GitHub issue** for security vulnerabilities.
2. Use [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability), or email the repository maintainers via the email listed in the GitHub profile.
3. Include as much detail as possible:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment** within 48 hours of your report.
- **Assessment** within 5 business days, confirming whether the issue is accepted or declined.
- **Fix timeline**: Critical vulnerabilities patched within 7 days. High-severity within 30 days.
- **Disclosure**: We follow coordinated disclosure. We credit reporters unless anonymity is requested.

## Security Practices

### Current Protections

- **SSRF prevention**: All URL-fetching scripts block private/internal IPs (`fetch_page.py`, `analyze_visual.py`)
- **Path traversal prevention**: Output paths validated against directory escapes (`capture_screenshot.py`, `parse_html.py`)
- **Bounded dependency pinning**: Version bounds with CVE-aware minimum versions
- **Non-root Docker**: Container scripts run as unprivileged `seouser`
- **No secrets in code**: API credentials stored in user config directories only

### Dependency Security

We track CVEs for all Python dependencies:

| Package | Minimum Version | CVE Coverage |
|---------|----------------|-------------|
| urllib3 | ≥2.6.3 | CVE-2026-21441 (CVSS 8.9), CVE-2025-66418 |
| requests | ≥2.32.4 | CVE-2024-47081, CVE-2024-35195 |
| lxml | ≥6.0.2 | CVE-2025-24928 + libxml2 patches |
| Pillow | ≥12.1.0 | CVE-2025-48379 |
| playwright | ≥1.56.0 | CVE-2025-59288 (optional) |

- Dependency updates automated via Dependabot (weekly).
- CI runs linting and tests on every pull request.

## Scope

**In scope:**
- Python scripts in `scripts/`
- Skill instructions that could lead to data leakage
- Docker configuration issues
- Dependency vulnerabilities
- SSRF bypasses

**Out of scope:**
- Third-party API security (DataForSEO, Google APIs)
- Claude Code platform vulnerabilities (report to Anthropic)
