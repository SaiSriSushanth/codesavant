# Use a stable base image
FROM python:3.10-bookworm

# Update and install basic tools first
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install other languages (split to avoid timeouts)
RUN apt-get update && apt-get install -y \
    ruby \
    php-cli \
    golang \
    openjdk-17-jdk \
    mono-complete \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash sandbox_user

WORKDIR /app
USER sandbox_user
CMD ["python3", "--version"]
