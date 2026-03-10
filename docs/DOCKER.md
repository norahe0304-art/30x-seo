# Docker Sandboxed Execution

Run 30x SEO Python scripts in a Docker container for extra isolation.

## Quick Start

### Build (without Playwright — lightweight)

```bash
cd 30x-seo
docker build -t 30x-seo-scripts .
```

### Build (with Playwright — includes Chromium)

```bash
docker build -f Dockerfile.playwright -t 30x-seo-scripts-pw .
```

## Usage

### Fetch a page

```bash
docker run --rm 30x-seo-scripts scripts/fetch_page.py https://example.com
```

### Parse HTML

```bash
docker run --rm 30x-seo-scripts scripts/parse_html.py https://example.com
```

### Capture screenshots (requires Playwright build)

```bash
docker run --rm -v "$(pwd)/screenshots:/app/screenshots" \
  30x-seo-scripts-pw scripts/capture_screenshot.py https://example.com --all
```

### Visual analysis (requires Playwright build)

```bash
docker run --rm 30x-seo-scripts-pw scripts/analyze_visual.py https://example.com --json
```

## Security

- Scripts run as non-root `seouser`
- No host filesystem access (except explicit volume mounts)
- Network access limited to outbound HTTP/HTTPS
- SSRF prevention still active inside container (private IP blocking)
