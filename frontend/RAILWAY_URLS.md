# How to Get Railway Public URLs

## Backend Public URL

1. Go to Railway Dashboard
2. Open your **Backend Service**
3. Go to **Settings** → **Networking**
4. You should see a domain like: `seraphanyarchive-production.up.railway.app`
5. Copy this URL (it should start with `https://`)

## Frontend Public URL

1. Go to Railway Dashboard
2. Open your **Frontend Service**
3. Go to **Settings** → **Networking**
4. Generate a domain or use the one provided
5. Copy this URL (it should start with `https://`)

## Update Environment Variables

### Frontend Service Variables:
- `VITE_API_BASE_URL` = `https://seraphanyarchive-production.up.railway.app` (your backend's PUBLIC URL)

### Backend Service Variables:
- `CORS_ORIGINS` = `https://your-frontend.railway.app` (your frontend's PUBLIC URL)
