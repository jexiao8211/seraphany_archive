# Running Database Migrations on Railway

## Method 1: Railway CLI (Recommended)

### Install Railway CLI
```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# Or download from: https://railway.app/cli
```

### Login and Connect
```bash
railway login
railway link  # Links to your Railway project
```

### Run Migrations
```bash
# From the backend directory
cd backend
railway run poetry run alembic upgrade head
```

This runs migrations in the Railway environment with all production environment variables.

---

## Method 2: Railway Dashboard Shell

### Steps:
1. Go to Railway Dashboard
2. Select your **Backend Service** (not the database)
3. Click on the **"Deployments"** tab
4. Click on the **latest deployment**
5. Look for **"Shell"** or **"Console"** button (usually in the top right)
6. Click it to open an interactive shell
7. Run:
   ```bash
   poetry run alembic upgrade head
   ```

**Note**: The Shell option might be in different places:
- Sometimes it's in the deployment details
- Sometimes it's in the service settings
- Sometimes it's called "Console" or "Terminal"

---

## Method 3: Add Migration to Startup (Automatic)

You can automatically run migrations when the app starts. This ensures migrations always run on deployment.

### Option A: Add to Procfile
Update `backend/Procfile`:
```
web: poetry run alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Option B: Add to startup script
Create `backend/start.sh`:
```bash
#!/bin/bash
poetry run alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Then update `Procfile`:
```
web: bash start.sh
```

**Warning**: This runs migrations on every deployment. Only use if you're comfortable with that.

---

## Method 4: Railway Scripts/Commands

Some Railway projects have a "Scripts" or "Commands" section where you can run one-off commands.

1. Go to your Backend Service
2. Look for "Scripts" or "Commands" tab
3. Add command: `poetry run alembic upgrade head`
4. Run it

---

## Troubleshooting

### "Shell not found"
- Railway's UI changes frequently
- Try looking for "Console", "Terminal", or "Run Command"
- Use Railway CLI (Method 1) as backup

### "Command not found"
- Make sure you're in the backend service (not database)
- Use full path: `poetry run alembic upgrade head`

### "Database connection failed"
- Check that DATABASE_URL is set automatically
- Verify database is in same Railway project
- Check service logs for connection errors

---

## Best Practice

**Recommended workflow:**
1. Run migrations manually first time (Method 1 or 2)
2. For future migrations, use Railway CLI (Method 1)
3. Only use automatic migrations (Method 3) if you're confident

**Why not always auto-run?**
- Migrations can fail and break deployment
- You want control over when migrations run
- Easier to debug issues if migrations run separately
