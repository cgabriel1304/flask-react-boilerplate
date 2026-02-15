# Stage 1: Build the React frontend
FROM node:22-alpine AS frontend-build

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci
COPY frontend/ .

# Build frontend assets
RUN mkdir -p /build-output
RUN npx vite build --outDir /build-output

# Stage 2: Python production image
FROM python:3.11-slim AS production

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy backend source code
COPY backend/ .

# Copy built frontend from stage 1
COPY --from=frontend-build /build-output ./public

# Set environment
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
