# Troubleshooting Railway Deployment

## 502 Error: "Application failed to respond"

This means Railway can't reach your app. Common causes:

### 1. Check Railway Logs
1. Go to Railway Dashboard
2. Click on your Backend Service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Check the "Logs" tab

Look for:
- Build errors
- Runtime errors
- Port binding issues
- Import errors

### 2. Common Issues

#### Issue: App not starting
**Symptoms**: No logs showing "Application startup complete"
**Solution**: Check that Procfile is correct and uvicorn is installed

#### Issue: Port binding error
**Symptoms**: "Address already in use" or port errors
**Solution**: Make sure Procfile uses `$PORT` not a hardcoded port

#### Issue: Import errors
**Symptoms**: "ModuleNotFoundError" or import failures
**Solution**: Check that all dependencies are in pyproject.toml

#### Issue: Database connection failed
**Symptoms**: Database connection errors in logs
**Solution**: Verify DATABASE_URL is set automatically (if DB is in same project)

### 3. Verify Procfile
Your Procfile should be:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4. Check Environment Variables
Make sure these are set:
- `DATABASE_URL` (auto-set if DB in same project)
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DEBUG=False`
- `PYTHON_ENV=production`

### 5. Test Locally First
Before deploying, test locally:
```bash
cd backend
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then visit: http://localhost:8000/docs

If this works locally but not on Railway, it's a deployment configuration issue.
