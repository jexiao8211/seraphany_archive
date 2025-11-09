#!/bin/bash
# Railway Migration Script
# Run this with: railway run bash railway_migrate.sh

echo "Running database migrations..."
poetry run alembic upgrade head
echo "Migrations complete!"
