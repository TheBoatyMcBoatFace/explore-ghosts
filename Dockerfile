# Use the official Python 3.11 base image
FROM python:3.11-slim

# Install system dependencies (for Chromium and Python environment)
RUN apt-get update && apt-get install -y \
    chromium wget gnupg2 ca-certificates \
    libnss3 libxss1 libatk1.0-0 libatk-bridge2.0-0 \
    libgbm-dev libasound2 libgtk-3-0 libdrm2 \
    fonts-liberation libappindicator3-1 libxcomposite1 \
    libxcursor1 libxdamage1 libxrandr2 libharfbuzz0b libgdk-pixbuf2.0-0 \
    libxshmfence1 libglu1-mesa libxi6 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Prevent Pyppeteer from downloading its own Chromium
ENV PUPPETEER_SKIP_DOWNLOAD=true

# Install Poetry (for managing Python dependencies)
RUN pip install pipx && pipx install poetry

# Set Python binaries in path
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy your code into the Docker image
COPY . .

# Install your app dependencies via Poetry
RUN poetry install

# Set up environment variables
ENV LOG_TIMEZONE="America/New_York"

# Default command to run the script
CMD ["poetry", "run", "python", "run.py"]
