# Setup Guide - Outreach Scraping Toolkit

This comprehensive guide will walk you through setting up the Outreach Scraping Preparation Toolkit from scratch.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Initial Setup](#initial-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Google Sheets API Setup](#google-sheets-api-setup)
6. [Apify API Setup](#apify-api-setup)
7. [Environment Configuration](#environment-configuration)
8. [Database Setup](#database-setup)
9. [Testing the Installation](#testing-the-installation)
10. [Production Deployment](#production-deployment)
11. [Common Issues](#common-issues)

---

## System Requirements

### Minimum Requirements

- **Operating System**: macOS, Linux, or Windows (with WSL recommended)
- **Python**: 3.9 or higher
- **Node.js**: 16.x or higher
- **npm**: 8.x or higher (comes with Node.js)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 1GB for dependencies and project files

### Recommended Setup

- **Python**: 3.10 or 3.11
- **Node.js**: 18.x LTS or 20.x LTS
- **Code Editor**: VS Code, PyCharm, or WebStorm
- **Terminal**: iTerm2 (macOS), Windows Terminal (Windows), or any modern terminal

### Check Installed Versions

```bash
# Check Python version
python3 --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check git version
git --version
```

---

## Initial Setup

### 1. Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/your-username/outreach-scraping-toolkit.git
cd outreach-scraping-toolkit

# Or using SSH
git clone git@github.com:your-username/outreach-scraping-toolkit.git
cd outreach-scraping-toolkit
```

### 2. Verify Project Structure

```bash
ls -la
```

You should see:
```
backend/
frontend/
config/
tools/
.env.example
.gitignore
init.sh
README.md
```

### 3. Make Init Script Executable

```bash
chmod +x init.sh
```

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment (Recommended)

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

Your terminal prompt should now show `(venv)` prefix.

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Apify Client (scraping)
- gspread (Google Sheets)
- Pydantic (data validation)
- PyYAML (configuration)
- python-dotenv (environment variables)

### 4. Verify Installation

```bash
python -c "import fastapi; print(fastapi.__version__)"
python -c "import apify_client; print('Apify client installed')"
python -c "import gspread; print('gspread installed')"
```

All commands should run without errors.

### 5. Return to Project Root

```bash
cd ..
```

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Node.js Dependencies

```bash
npm install
```

This will install:
- React (UI framework)
- Vite (build tool)
- Tailwind CSS (styling)
- TypeScript (type safety)
- React Router (navigation)

**Installation may take 2-5 minutes depending on your internet connection.**

### 3. Verify Installation

```bash
npm list react react-dom vite
```

Should show installed versions without errors.

### 4. Return to Project Root

```bash
cd ..
```

---

## Google Sheets API Setup

To export data to Google Sheets, you need to set up a Google Cloud project and enable the Sheets API.

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Sign in with your Google account
3. Click "Select a project" dropdown at the top
4. Click "NEW PROJECT"
5. Enter project name: `Outreach Scraping Toolkit`
6. Click "CREATE"

### Step 2: Enable Google Sheets API

1. In the Google Cloud Console, go to **APIs & Services > Library**
2. Search for "Google Sheets API"
3. Click on "Google Sheets API"
4. Click "ENABLE"

### Step 3: Create Service Account

1. Go to **APIs & Services > Credentials**
2. Click "CREATE CREDENTIALS" > "Service account"
3. Fill in details:
   - **Service account name**: `outreach-toolkit-service`
   - **Service account ID**: (auto-generated)
   - **Description**: "Service account for Outreach Scraping Toolkit"
4. Click "CREATE AND CONTINUE"
5. For role, select: **Editor** (or **Basic > Editor**)
6. Click "CONTINUE"
7. Click "DONE"

### Step 4: Create and Download JSON Key

1. In the **Credentials** page, find your service account in the list
2. Click on the service account email
3. Go to the **KEYS** tab
4. Click "ADD KEY" > "Create new key"
5. Select **JSON** format
6. Click "CREATE"
7. The JSON key file will download automatically

### Step 5: Save Credentials to Project

1. Rename the downloaded file to `google-credentials.json`
2. Move it to the `config/` directory in your project:

```bash
mv ~/Downloads/your-project-*.json ./config/google-credentials.json
```

3. Verify the file is in place:

```bash
ls -la config/google-credentials.json
```

### Step 6: Note the Service Account Email

Open the JSON file and find the `client_email` field:

```bash
cat config/google-credentials.json | grep client_email
```

Example output:
```
"client_email": "outreach-toolkit-service@your-project.iam.gserviceaccount.com"
```

**Important**: You'll need to share any Google Sheets you want to write to with this email address.

---

## Apify API Setup

Apify is used for web scraping. For development, the app can work without Apify (using mock data), but for production you'll need an API key.

### Step 1: Create an Apify Account

1. Go to [apify.com](https://apify.com)
2. Click "Sign up" or "Start free"
3. Complete the registration process
4. Verify your email address

### Step 2: Get Your API Token

1. Log in to your Apify account
2. Go to **Settings** > **Integrations**
3. Find your **Personal API token** or create a new one
4. Click "Copy" to copy the token

### Step 3: Save API Token (Optional for Development)

The app includes mock data, so you can test without Apify. To use real scraping:

1. Copy your API token
2. Add it to your `.env` file (see Environment Configuration section)

**Free Tier Limits:**
- Apify provides a free tier with limited usage
- Approximately $5 worth of free platform credits per month
- Suitable for testing and small-scale projects

---

## Environment Configuration

### 1. Copy Example Environment File

```bash
cp .env.example .env
```

### 2. Edit .env File

Open `.env` in your text editor:

```bash
# Use your preferred editor
nano .env
# or
vim .env
# or
code .env  # VS Code
```

### 3. Configure Variables

```env
# ============================================================
# Apify API Configuration
# ============================================================
# Optional for development (mock data will be used if not set)
# Get your key from: https://console.apify.com/account/integrations
APIFY_API_KEY=your_apify_api_key_here

# ============================================================
# Google Sheets Configuration
# ============================================================
# Path to your Google service account JSON credentials
GOOGLE_SHEETS_CREDENTIALS_PATH=./config/google-credentials.json

# Enable/disable Google Sheets export functionality
GOOGLE_SHEETS_ENABLED=true

# ============================================================
# Backend Configuration
# ============================================================
# Host for backend server (0.0.0.0 allows external access)
BACKEND_HOST=0.0.0.0

# Port for backend server
BACKEND_PORT=8000

# ============================================================
# Frontend Configuration
# ============================================================
# Frontend URL for CORS configuration
FRONTEND_URL=http://localhost:5173

# ============================================================
# Scraping Configuration
# ============================================================
# Maximum number of profiles to scrape per platform (rate limiting)
MAX_LINKEDIN_PROFILES=100
MAX_INSTAGRAM_PROFILES=100

# Delay between requests in seconds (avoid rate limiting)
RATE_LIMIT_DELAY=2

# ============================================================
# Logging Configuration
# ============================================================
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO
```

### 4. Save and Close

Press `Ctrl + O` then `Enter` to save (in nano), or `:wq` (in vim).

### 5. Verify Configuration

```bash
cat .env
```

Ensure no syntax errors and all paths are correct.

---

## Database Setup

This project uses **Google Sheets as a database**, so no traditional database setup is required.

### In-Memory Storage

- Scraped results are stored in memory during runtime
- Results persist until the backend server is restarted
- For permanent storage, export to Google Sheets or download as CSV

### Future Database Integration

If you want to add persistent storage:

1. **SQLite** (simplest):
   ```bash
   pip install sqlalchemy sqlite3
   ```

2. **PostgreSQL** (production):
   ```bash
   pip install psycopg2-binary sqlalchemy
   ```

3. **MongoDB** (NoSQL):
   ```bash
   pip install pymongo motor
   ```

---

## Testing the Installation

### 1. Test Backend

**Option A: Using init.sh**

```bash
./init.sh
# Select option 2: Run backend only
```

**Option B: Manually**

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
✅ Services initialized successfully
INFO:     Application startup complete.
```

**Test the backend:**

Open another terminal and run:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-05T10:30:00.123456",
  "services": {
    "scraper": true,
    "sheets": true
  }
}
```

### 2. Test Frontend

**In a new terminal:**

```bash
cd frontend
npm run dev
```

Expected output:
```
  VITE v5.3.4  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Test the frontend:**

Open your browser and navigate to [http://localhost:5173](http://localhost:5173)

You should see the Outreach Scraping Toolkit dashboard.

### 3. Test API Endpoints

With backend running, test key endpoints:

**Get audience configuration:**

```bash
curl http://localhost:8000/api/config/audience
```

**Test scraping (with mock data):**

```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["LinkedIn"],
    "industries": ["AI"],
    "roles": ["Founder"],
    "regions": ["Germany"]
  }'
```

**Get results:**

```bash
curl http://localhost:8000/api/results?limit=10
```

### 4. Test Google Sheets Export (Optional)

1. Create a test Google Sheet
2. Share it with your service account email (from google-credentials.json)
3. In the UI, click "Export to Sheet"
4. Verify data appears in the Google Sheet

---

## Production Deployment

### Backend Deployment

**Using Uvicorn with Gunicorn:**

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

**Using Docker:**

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t outreach-backend .
docker run -p 8000:8000 --env-file ../.env outreach-backend
```

### Frontend Deployment

**Build for production:**

```bash
cd frontend
npm run build
```

This creates a `dist/` folder with optimized static files.

**Serve with a static server:**

```bash
npm install -g serve
serve -s dist -p 3000
```

**Deploy to Vercel, Netlify, or similar:**

```bash
# Vercel
npm install -g vercel
vercel

# Netlify
npm install -g netlify-cli
netlify deploy --prod
```

### Environment Variables for Production

Create a production `.env` file:

```env
# Use production URLs
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=https://your-frontend-domain.com

# Use absolute paths for credentials
GOOGLE_SHEETS_CREDENTIALS_PATH=/app/config/google-credentials.json

# Production logging
LOG_LEVEL=WARNING

# Rate limiting (more conservative)
MAX_LINKEDIN_PROFILES=50
MAX_INSTAGRAM_PROFILES=50
RATE_LIMIT_DELAY=5
```

---

## Common Issues

### Issue: Port Already in Use

**Symptom:**
```
ERROR:    [Errno 48] Address already in use
```

**Solution:**

Find and kill the process using the port:

```bash
# Find process on port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

Or use a different port:

```bash
uvicorn main:app --port 8001
```

### Issue: Google Credentials Not Found

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: './config/google-credentials.json'
```

**Solution:**

1. Verify file exists:
   ```bash
   ls -la config/google-credentials.json
   ```

2. Check .env path is correct:
   ```bash
   cat .env | grep GOOGLE_SHEETS_CREDENTIALS_PATH
   ```

3. Use absolute path if relative path fails:
   ```bash
   GOOGLE_SHEETS_CREDENTIALS_PATH=/full/path/to/config/google-credentials.json
   ```

### Issue: Module Not Found

**Symptom:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**

1. Ensure virtual environment is activated:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Issue: Frontend Can't Connect to Backend

**Symptom:**
- Network errors in browser console
- "Failed to fetch" errors

**Solution:**

1. Verify backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check CORS settings in `backend/main.py`:
   ```python
   allow_origins=["*"]  # Should allow all origins for development
   ```

3. Create `frontend/.env.local`:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. Restart frontend:
   ```bash
   npm run dev
   ```

### Issue: Google Sheets Permission Denied

**Symptom:**
```
gspread.exceptions.APIError: PERMISSION_DENIED
```

**Solution:**

1. Find your service account email:
   ```bash
   cat config/google-credentials.json | grep client_email
   ```

2. Share the Google Sheet with that email address

3. Grant "Editor" permissions

### Issue: npm install Fails

**Symptom:**
```
npm ERR! code EACCES
npm ERR! syscall access
```

**Solution:**

**Option 1: Fix npm permissions (recommended)**

```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

**Option 2: Use sudo (not recommended)**

```bash
sudo npm install
```

**Option 3: Reinstall Node.js using nvm**

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install Node.js
nvm install 18
nvm use 18

# Reinstall dependencies
npm install
```

---

## Next Steps

After completing setup:

1. **Read the [README.md](./README.md)** for usage instructions
2. **Explore the [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** for API details
3. **Run the cost estimation tool** (see [COST_ESTIMATION_GUIDE.md](./COST_ESTIMATION_GUIDE.md))
4. **Test scraping with mock data** before using Apify
5. **Customize audience filters** in `config/audience.yaml`

---

## Support

If you encounter issues not covered here:

1. Check the [README.md Troubleshooting section](./README.md#troubleshooting)
2. Search [GitHub Issues](https://github.com/your-username/outreach-scraping-toolkit/issues)
3. Open a new issue with:
   - Detailed error message
   - Steps to reproduce
   - Environment details (OS, Python version, Node version)

---

**Setup Complete!** You're ready to start using the Outreach Scraping Toolkit.
