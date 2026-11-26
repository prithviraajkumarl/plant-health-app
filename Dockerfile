# Plant Health Detection App - Production Container for Hugging Face Spaces / Render / Cloud
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860 \
    HOME=/home/user

# Install minimal OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security (UID 1000 required for Hugging Face Spaces)
RUN useradd -m -u 1000 user
WORKDIR /home/user/app

# Install Python requirements
COPY --chown=user:user app/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=user:user app/ app/
COPY --chown=user:user docs/ docs/

# Ensure directories for SQLite database and uploads exist with correct permissions
RUN mkdir -p app/db app/uploads app/uploads/thumbs app/runtime && \
    chown -R user:user /home/user/app

# Switch to non-root user
USER user

# Hugging Face Spaces uses port 7860 by default; Render uses $PORT
EXPOSE 7860

# Launch server
CMD ["sh", "-c", "python -m uvicorn app.backend.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
