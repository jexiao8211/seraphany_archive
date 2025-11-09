#!/bin/sh
# Entrypoint script for Railway frontend deployment

# Use PORT from environment or default to 8080
PORT=${PORT:-8080}

echo "Starting frontend server on port $PORT"

# Run serve with the port
exec serve -s dist -l tcp://0.0.0.0:$PORT
