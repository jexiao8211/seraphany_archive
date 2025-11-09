#!/bin/bash
# Entrypoint script for Railway deployment

# Railway should set PORT, but default to 8080 if not set
PORT=${PORT:-8080}

echo "Starting application on port $PORT"
echo "PORT environment variable: ${PORT}"

# Run uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
