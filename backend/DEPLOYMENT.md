# Backend Deployment Guide for Railway

## Prerequisites
- Railway account (railway.app)
- GitHub repository with your code
- Production database already set up on Railway

## Deployment Steps

### 1. Connect Repository to Railway
1. Go to Railway dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the `backend` folder as the root directory

### 2. Configure Environment Variables
In Railway, add these environment variables:

**Required:**
- `DATABASE_URL` - Your PostgreSQL connection string (Railway auto-provides this if database is in same project)
- `SECRET_KEY` - Your production secret key (from .env.production)
- `JWT_SECRET_KEY` - Your JWT secret key (from .env.production)
- `DEBUG` - Set to `False`
- `PYTHON_ENV` - Set to `production`

**CORS Configuration:**
- `CORS_ORIGINS` - JSON array: `["https://your-frontend-domain.netlify.app"]`

**Upload Configuration:**
- `UPLOAD_DIR` - Set to `./uploads`
- `MAX_FILE_SIZE` - Set to `5242880` (5MB)
- `ALLOWED_EXTENSIONS` - Set to `jpg,jpeg,png,webp`

### 3. Railway Auto-Detection
Railway will automatically:
- Detect Python/Poetry project
- Install dependencies from `pyproject.toml`
- Run the app using the Procfile

### 4. Link Database
1. In Railway project, click "New" → "Database" → "PostgreSQL" (if not already created)
2. Railway will automatically set `DATABASE_URL` environment variable
3. Your app will connect automatically

### 5. Run Migrations
After deployment, run migrations:
1. Go to your backend service in Railway
2. Click "Deployments" tab
3. Click on the latest deployment
4. Open "Shell" or "Logs"
5. Run: `poetry run alembic upgrade head`

Or use Railway's CLI:
```bash
railway run poetry run alembic upgrade head
```

### 6. Get Your Backend URL
1. In Railway, click on your backend service
2. Go to "Settings" → "Networking"
3. Generate a domain (or use custom domain)
4. Copy the URL (e.g., `https://your-app.railway.app`)

### 7. Update Frontend
Update your frontend `.env.production` with the Railway backend URL:
```
VITE_API_BASE_URL=https://your-app.railway.app
```

## Troubleshooting

**Build fails:**
- Check that `pyproject.toml` is in the backend root
- Verify Python version in `runtime.txt`

**Database connection fails:**
- Ensure database is in same Railway project
- Check `DATABASE_URL` environment variable

**App crashes:**
- Check logs in Railway dashboard
- Verify all environment variables are set
- Check that port is set to `$PORT` (Railway provides this)

## Post-Deployment Checklist
- [ ] Backend is accessible at Railway URL
- [ ] Database migrations ran successfully
- [ ] API endpoints respond correctly
- [ ] CORS is configured for frontend domain
- [ ] Environment variables are set correctly
