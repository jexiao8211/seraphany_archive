# Railway Migration Script for Windows
# Run this with: railway run powershell railway_migrate.ps1

Write-Host "Running database migrations..." -ForegroundColor Green
poetry run alembic upgrade head
Write-Host "Migrations complete!" -ForegroundColor Green
