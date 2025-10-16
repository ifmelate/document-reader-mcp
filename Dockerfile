FROM python:3.10-slim

# Create non-root user
RUN groupadd -r mcpuser && useradd -r -g mcpuser -u 1000 mcpuser

# Set working directory
WORKDIR /app

# Install system dependencies (if needed for document processing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server/ ./server/

# Create directory for documents (optional mount point)
RUN mkdir -p /documents

# Change ownership to non-root user
RUN chown -R mcpuser:mcpuser /app /documents

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DOC_READER_RATE_LIMIT_PER_MINUTE=60

# Switch to non-root user
USER mcpuser

# Run the MCP server
CMD ["python", "-m", "server.main"]

