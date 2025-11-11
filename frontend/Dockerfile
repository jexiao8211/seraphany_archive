# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Railway automatically passes environment variables to Docker builds as ENV
# We also accept them as ARG in case Railway passes them as build arguments
ARG VITE_API_BASE_URL
ARG NODE_ENV=production

# Set as environment variables so Vite can access them during build
# Use ARG value if provided, otherwise Railway's ENV will be used
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV NODE_ENV=${NODE_ENV:-production}

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Debug: Print environment variables during build
# Check both ARG and ENV (Railway might pass as either)
RUN echo "=== Build-time Environment Variables ===" && \
    echo "ARG VITE_API_BASE_URL=${VITE_API_BASE_URL:-NOT_SET}" && \
    echo "ENV VITE_API_BASE_URL=${VITE_API_BASE_URL:-NOT_SET}" && \
    echo "NODE_ENV=${NODE_ENV:-NOT_SET}" && \
    echo "========================================="

# Create .env.production file from environment variable
# This ensures Vite can access it during build even if ARG wasn't passed
# Railway should pass env vars automatically, but this is a fallback
RUN if [ -n "$VITE_API_BASE_URL" ] && [ "$VITE_API_BASE_URL" != "NOT_SET" ]; then \
      echo "VITE_API_BASE_URL=$VITE_API_BASE_URL" > .env.production && \
      echo "✅ Created .env.production with VITE_API_BASE_URL=$VITE_API_BASE_URL"; \
    else \
      echo "❌ WARNING: VITE_API_BASE_URL not set! Build will use fallback (localhost:8000)."; \
      echo "   Make sure VITE_API_BASE_URL is set in Railway → Variables"; \
    fi

# Build the app
# Vite will embed VITE_* environment variables at build time
# It will read from .env.production if available, or from ENV vars
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Install serve to run the static files
RUN npm install -g serve

# Copy built files from builder
COPY --from=builder /app/dist ./dist

# Copy and make entrypoint script executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8080

# Use entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
