# Setup Guide - Outreach Scraping Toolkit

Complete installation and configuration guide for the Outreach Scraping Toolkit.

## Prerequisites

Before installing the toolkit, ensure you have the following software installed:

### Required Software

- **Python 3.9 or higher**
  - Check version: `python --version` or `python3 --version`
  - Download: [python.org](https://www.python.org/downloads/)

- **Node.js 16.x or higher**
  - Check version: `node --version`
  - Download: [nodejs.org](https://nodejs.org/)

- **npm 8.x or higher**
  - Check version: `npm --version`
  - Comes bundled with Node.js

- **pip (Python package manager)**
  - Check version: `pip --version` or `pip3 --version`
  - Usually comes with Python installation

### System Requirements

- **Operating System:** macOS, Linux, or Windows (WSL recommended for Windows)
- **Memory:** Minimum 2GB RAM available
- **Disk Space:** 500MB free space for dependencies and data
- **Network:** Internet connection for API calls and package installation

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd my-app
```

### 2. Environment Configuration

The toolkit requires an Apify API token for web scraping functionality.

#### Get Your Apify API Token

1. Create a free account at [apify.com](https://apify.com)
2. Navigate to **Settings > Integrations > API & Webhooks**
3. Copy your **Personal API Token**

#### Configure Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit the `.env` file and add your Apify token:

```bash
APIFY_API_TOKEN=your_actual_apify_token_here
```

**Important:** Never commit the `.env` file to version control. It's already in `.gitignore`.

### 3. Install Dependencies

#### Option A: Automated Setup (Recommended)

Use the provided init script for one-command setup:

```bash
chmod +x init.sh
./init.sh
```

The script will:
- Install backend Python dependencies
- Install frontend Node.js dependencies
- Start the backend server on port 8000
- Start the frontend dev server on port 5173

#### Option B: Manual Setup

If you prefer manual installation or the script doesn't work:

**Backend Setup:**

```bash
cd backend
pip install -r requirements.txt
# Or if using pip3:
pip3 install -r requirements.txt
```

**Frontend Setup:**

```bash
cd frontend
npm install
```

## Running the Application

### Using the Init Script

```bash
chmod +x init.sh
./init.sh
```

This will start both servers in the background. Press `Ctrl+C` to stop both services.

### Manual Startup

**Terminal 1 - Backend:**

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

### Accessing the Application

Once both servers are running:

- **Frontend Dashboard:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs (Interactive Swagger UI)
- **Health Check:** http://localhost:8000/ (Returns API status)

## Configuration

### Audience Targeting

Edit `config/audience.yaml` to customize your target audience:

```yaml
industries:
  - AI
  - Web3
  - blockchain
  - tech startups

roles:
  - Founders
  - CEOs
  - Co-founders
  - BD heads
  - Product Owners
  - Growth Leads

regions:
  - Germany
  - broader EU
  - South Asia
  - Southeast Asia

platforms:
  - LinkedIn
  - X
  - Telegram
  - TikTok
```

Changes to this file take effect immediately (no restart required for backend with `--reload` flag).

### Backend Configuration

The backend automatically loads configuration from `.env`. Available options:

```bash
# Required
APIFY_API_TOKEN=your_token_here

# Optional (future features)
# LINKEDIN_API_TOKEN=your_linkedin_token
# TWITTER_API_KEY=your_twitter_key
# OPENAI_API_KEY=your_openai_key
```

## Verification

### 1. Check Backend is Running

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "status": "ok",
  "message": "Outreach Scraping Toolkit API is running",
  "version": "1.0.0"
}
```

### 2. Check Frontend is Running

Open http://localhost:5173 in your browser. You should see the dashboard with:
- Dark sidebar on the left
- Search form and results table in the center
- Detail panel on the right (when a lead is selected)

### 3. Test API Documentation

Visit http://localhost:8000/docs to see interactive API documentation. You can test endpoints directly from this interface.

### 4. Test Scraping (Optional)

In the frontend:
1. Enter a search query (e.g., "AI startups")
2. Enter a city (e.g., "Berlin")
3. Enter a state/region (e.g., "Germany")
4. Click "Scrape Leads"

If your Apify token is not configured, you'll see mock data (this is expected behavior).

## Troubleshooting

### Backend Won't Start

**Problem:** `ModuleNotFoundError` or missing dependencies

**Solution:**
```bash
cd backend
pip install -r requirements.txt --upgrade
# Or
pip3 install -r requirements.txt --upgrade
```

**Problem:** `Address already in use` on port 8000

**Solution:**
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
# Then: taskkill /PID <pid> /F

# Restart backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Problem:** `uvicorn: command not found`

**Solution:**
```bash
# Ensure uvicorn is installed
pip install uvicorn[standard]

# Or run with python -m
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Won't Start

**Problem:** `Module not found` or npm errors

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Problem:** `Port 5173 is already in use`

**Solution:**
```bash
# macOS/Linux
lsof -ti:5173 | xargs kill -9

# Windows
netstat -ano | findstr :5173
# Then: taskkill /PID <pid> /F

# Restart frontend
cd frontend
npm run dev
```

**Problem:** `npm: command not found`

**Solution:**
Install Node.js from [nodejs.org](https://nodejs.org/), which includes npm.

### Scraping Issues

**Problem:** "Invalid API token" or authentication errors

**Solution:**
1. Verify `.env` file exists in project root (not in `backend/` directory)
2. Check token format: `APIFY_API_TOKEN=apify_api_xxx...`
3. Verify token at [Apify Console](https://console.apify.com/account/integrations)
4. Restart backend after updating `.env`

**Problem:** No results found for search

**Solution:**
1. Try broader search terms (e.g., "restaurants" vs "vegan restaurants")
2. Use major cities or well-known locations
3. Increase `max_results` parameter
4. Check Apify account has sufficient credits
5. Verify search location exists in Google Maps

**Problem:** Mock data is returned instead of real data

**Solution:**
This is expected if:
- `APIFY_API_TOKEN` is not set in `.env`
- Token is set to placeholder value `your_apify_api_token_here`
- Apify API call fails (falls back to mock data gracefully)

To use real data, ensure you have a valid Apify token configured.

### CORS Errors

**Problem:** Browser console shows `Access-Control-Allow-Origin` errors

**Solution:**
1. Ensure backend is running on port 8000
2. Check CORS middleware in `backend/main.py` (should allow all origins in dev)
3. Clear browser cache and hard reload (Cmd+Shift+R / Ctrl+Shift+R)
4. Try in incognito/private browsing mode

### Data Storage Issues

**Problem:** History or Bookmarks not saving

**Solution:**
```bash
# Ensure data directory exists
mkdir -p data
chmod -R 755 data

# Check for JSON files
ls -la data/
# Should see: history.json, leads.json
```

**Problem:** Permission denied when writing files

**Solution:**
```bash
# Fix permissions
chmod -R 755 data
chmod 644 data/*.json
```

### Python Version Issues

**Problem:** `SyntaxError` or features not supported

**Solution:**
Ensure Python 3.9+ is installed:
```bash
python --version
# If < 3.9, upgrade Python

# Use specific Python version
python3.9 -m pip install -r requirements.txt
python3.9 -m uvicorn main:app --reload
```

### Environment Not Loading

**Problem:** `.env` file exists but values aren't loaded

**Solution:**
1. Ensure `.env` is in project root directory
2. Check file format (no quotes around values usually):
   ```bash
   APIFY_API_TOKEN=apify_api_xxx
   ```
3. Restart backend completely (stop and start, not just reload)
4. Check for BOM or encoding issues:
   ```bash
   file .env  # Should show "ASCII text" or "UTF-8"
   ```

## Next Steps

- Read [API.md](./API.md) for complete API documentation
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) to understand system design
- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
- See [../CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines

## Support

- **Issues:** Create an issue in the repository
- **API Docs:** http://localhost:8000/docs (when backend is running)
- **Cost Analysis:** See [COST_ESTIMATION.md](./COST_ESTIMATION.md)
