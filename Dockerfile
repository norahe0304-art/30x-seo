FROM python:3.12-slim

LABEL org.opencontainers.image.title="30x-seo-scripts"
LABEL org.opencontainers.image.description="Sandboxed execution for 30x SEO Python scripts"

# Security: non-root user
RUN useradd --create-home --shell /bin/bash seouser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts only
COPY scripts/ ./scripts/

# Drop to non-root
USER seouser

# No default entrypoint — caller specifies which script to run
ENTRYPOINT ["python3"]
