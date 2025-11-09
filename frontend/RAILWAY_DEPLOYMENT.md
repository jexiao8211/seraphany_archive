# Frontend Deployment Guide for Railway

## Prerequisites
- Railway account (railway.app)
- GitHub repository with your code
- Backend already deployed on Railway

## Deployment Steps

### 1. Update Environment Variables

**Update `frontend/.env.production`** with your Railway backend URL:
```
VITE_API_BASE_URL=https://seraphanyarchive-production.up.railway.app
VITE_DEBUG=false
VITE_LOG_LEVEL=error
VITE_ENABLE_DEBUG_TOOLS=false
VITE_ENABLE_MOCK_DATA=false
VITE_NODE_ENV=production
```

### 2. Deploy to Railway

1. **Go to Railway Dashboard**
2. **Open your existing project** (the one with your backend)
3. **Click "New" → "GitHub Repo"**
4. **Select your repository**
5. **Important:** Set root directory to `frontend`
6. **Railway will auto-detect** it's a Node.js project

### 3. Configure Environment Variables

In Railway, go to your Frontend Service → Variables:

**Required:**
- `VITE_API_BASE_URL` = `https://seraphanyarchive-production.up.railway.app`
- `VITE_NODE_ENV` = `production`
- `NODE_ENV` = `production`

### 4. Railway Auto-Detection

Railway will:
- Detect Node.js project
- Run `npm install`
- Run `npm run build` (from package.json)
- Serve the `dist` folder using the Dockerfile

### 5. Get Your Frontend URL

1. In Railway, click on your Frontend Service
2. Go to "Settings" → "Networking"
3. Generate a domain (e.g., `your-frontend.railway.app`)
4. Copy this URL

### 6. Update Backend CORS

1. Go to Railway → Backend Service → Variables
2. Update `CORS_ORIGINS` to include your frontend URL:
   ```
   CORS_ORIGINS=https://your-frontend.railway.app
   ```
   Or if you have multiple origins:
   ```
   CORS_ORIGINS=https://your-frontend.railway.app,https://your-custom-domain.com
   ```
3. Railway will automatically redeploy

### 7. Test Your Deployment

1. Visit your Railway frontend URL
2. Try logging in/registering
3. Browse products
4. Test the full flow

## Troubleshooting

### Build Fails
- Check that `package.json` has `build` script
- Verify root directory is set to `frontend`
- Check build logs for errors

### App Doesn't Load
- Verify `dist` folder is being created
- Check that serve is installed (in Dockerfile)
- Check Railway logs

### API Connection Fails
- Verify `VITE_API_BASE_URL` is set correctly
- Check backend CORS includes your Railway frontend domain
- Check browser console for CORS errors

## Advantages of Railway for Frontend

- ✅ Everything in one place
- ✅ Same billing/account
- ✅ Easier to manage
- ✅ Private networking between services

## Note

Railway uses Docker for deployment, so the Dockerfile handles:
1. Building your React app
2. Installing `serve` to run static files
3. Serving the built files on the PORT Railway provides
