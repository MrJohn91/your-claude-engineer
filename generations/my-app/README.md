# Outreach Scraping Toolkit

A complete outreach lead generation toolkit with a professional web UI for scraping and managing leads from multiple platforms. Built for agencies, entrepreneurs, and B2B sales teams to efficiently find and manage high-quality leads.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![React](https://img.shields.io/badge/react-18.3-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

1. **Target Audience Configuration System** - YAML-based targeting for industries, roles, regions, and platforms
2. **Data Pipeline & API Backend** - FastAPI REST API with 10+ endpoints for comprehensive lead management
3. **Professional Web UI Dashboard** - Modern React interface with 3-column layout: navigation, results table, and lead details
4. **Cost Estimation Tool** - Complete cost analysis for scraping operations at various scales (1k-100k leads/month)
5. **Web Scraping Integration** - Apify-powered Google Maps scraper with graceful fallback to mock data
6. **Complete Documentation** - Comprehensive setup guides, API reference, architecture docs, and deployment guides

## What It Does

The Outreach Scraping Toolkit helps you:
- **Find leads:** Search for businesses and companies using Google Maps data
- **Manage contacts:** Bookmark high-priority leads and track search history
- **Export data:** Download results as CSV for use in CRM systems
- **Estimate costs:** Analyze scraping costs at different scales
- **Target audiences:** Configure industries, roles, regions, and platforms to focus on

## Tech Stack

- **Backend:** FastAPI (Python 3.9+) with REST API endpoints
- **Frontend:** React 18 + Vite + Tailwind CSS
- **Scraping:** Apify API integration (Google Maps Scraper)
- **Config:** YAML-based audience targeting
- **Storage:** File-based JSON storage (bookmarks, history)
- **UI Components:** Custom components with Lucide icons

## System Requirements

- **Python:** 3.9 or higher
- **Node.js:** 16.x or higher
- **npm:** 8.x or higher
- **Operating System:** macOS, Linux, or Windows (with WSL recommended)
- **Memory:** Minimum 2GB RAM
- **Disk Space:** 500MB free space

## Quick Start

### 1. Clone and Navigate

```bash
git clone <your-repo-url>
cd my-app
```

### 2. Set Up Environment Variables

Copy the example environment file and add your Apify API token:

```bash
cp .env.example .env
```

Edit `.env` and add your Apify API token:

```
APIFY_API_TOKEN=your_apify_api_token_here
```

**To get your Apify API token:**
1. Sign up at [apify.com](https://apify.com)
2. Go to Settings > Integrations > API & Webhooks
3. Copy your API token
4. Paste it into the `.env` file

### 3. Run the Application

Use the automated setup script:

```bash
chmod +x init.sh
./init.sh
```

The script will:
- Install backend dependencies (FastAPI, Apify client, etc.)
- Install frontend dependencies (React, Vite, Tailwind)
- Start the backend server on port 8000
- Start the frontend dev server on port 5173

**Access the application:**
- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Manual Installation

If you prefer to set up manually or the init script doesn't work:

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173

## Configuration

### Target Audience Configuration

Edit `config/audience.yaml` to define your target audience:

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

The configuration is loaded by the backend API and available at `/api/config/audience`.

## Usage Examples

### 1. Running a Scraping Operation

1. Open the dashboard at http://localhost:5173
2. In the "Scrape Leads" form, fill in:
   - **Keyword:** e.g., "AI startups", "blockchain companies"
   - **City:** e.g., "Berlin", "Singapore"
   - **State/Region:** e.g., "Germany", "Singapore"
   - **Max Results:** 20 (or any number up to 100)
3. Click "Scrape Leads"
4. Wait for results to load in the table below

**The scraper will:**
- Use Apify's Google Maps Scraper to find businesses
- Filter based on your target audience configuration
- Return business details including name, rating, address, phone, website

### 2. Exporting Results to CSV

After scraping leads:

1. Review the results in the table
2. Click the "Export CSV" button above the results table
3. A CSV file will download with all lead data
4. Open in Excel, Google Sheets, or any CSV-compatible tool

**CSV includes:**
- Name
- Rating
- Review Count
- Address
- Phone
- Website
- Place ID

### 3. Viewing and Managing Search History

1. Click "History" in the left sidebar
2. View all previous scraping operations with:
   - Search parameters (keyword, city, state)
   - Result count
   - Timestamp
3. Click "Rerun Search" to repeat any previous scraping operation
4. Click "Delete" to remove history entries

### 4. Bookmarking and Managing Leads

1. In the results table, click on any lead row
2. The lead detail panel opens on the right side
3. Click the "Bookmark" button (star icon) to save the lead
4. Navigate to "Bookmarks" in the left sidebar to view all saved leads
5. Click "Remove" to unbookmark a lead

**Use bookmarks for:**
- Saving high-priority leads for follow-up
- Creating curated lists for specific campaigns
- Organizing leads by quality or priority

### 5. Accessing Cost Insights

1. Click "Cost Insights" in the left sidebar
2. View comprehensive cost analysis including:
   - Cost breakdown by category (Apify, Proxies, APIs, AI, Infrastructure)
   - Pricing for different scales (1k, 10k, 50k leads/month)
   - ROI analysis and revenue potential
   - Cost optimization strategies

**Use cost insights for:**
- Budgeting your scraping operations
- Pricing your lead generation services
- Optimizing cost per lead
- Planning for scale

## API Endpoints

The backend provides the following REST API endpoints:

### Configuration

- `GET /api/config/audience` - Get target audience configuration

### Scraping

- `POST /api/scrape` - Scrape leads from Google Maps
  - Body: `{"keyword": "AI startups", "city": "Berlin", "state": "Germany", "max_results": 20}`
  - Returns: Array of leads with business details

### History Management

- `GET /api/history` - Get all search history
- `POST /api/history` - Add search to history
- `DELETE /api/history/{history_id}` - Delete history entry

### Bookmark Management

- `GET /api/bookmarks` - Get all bookmarked leads
- `POST /api/bookmarks` - Add lead to bookmarks
- `DELETE /api/bookmarks/{lead_id}` - Remove bookmark

### Export

- `GET /api/export/csv` - Export leads to CSV format

**Interactive API Documentation:** http://localhost:8000/docs

## Troubleshooting

### Backend won't start

**Problem:** `ModuleNotFoundError` or dependency errors

**Solution:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

**Problem:** `Address already in use` on port 8000

**Solution:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9
# Restart backend
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend won't start

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
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
# Restart frontend
cd frontend && npm run dev
```

### Scraping fails or returns no results

**Problem:** "Invalid API token" or authentication errors

**Solution:**
1. Check `.env` file has correct `APIFY_API_TOKEN`
2. Verify token at https://console.apify.com/account/integrations
3. Restart backend after updating `.env`

**Problem:** No results found for search

**Solution:**
1. Try broader search terms (e.g., "restaurants" instead of "vegan restaurants")
2. Use larger cities or well-known locations
3. Increase `max_results` to get more data
4. Check Apify account has sufficient credits

### CORS errors in browser console

**Problem:** `Access-Control-Allow-Origin` errors

**Solution:**
- Ensure backend is running on port 8000
- Check backend CORS settings in `backend/main.py`
- Clear browser cache and reload

### No data in History or Bookmarks

**Problem:** History/Bookmarks appear empty

**Solution:**
1. Check `data/` directory exists in project root
2. Verify write permissions: `chmod -R 755 data/`
3. Check backend logs for file write errors

## Documentation

Complete documentation is available in the `docs/` directory:

- **[Setup Guide](docs/SETUP.md)** - Detailed installation and configuration instructions
- **[API Reference](docs/API.md)** - Complete REST API documentation with examples
- **[Architecture](docs/ARCHITECTURE.md)** - System design and technical architecture
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions
- **[Cost Estimation](docs/COST_ESTIMATION.md)** - Detailed cost analysis and pricing
- **[Contributing](CONTRIBUTING.md)** - Guidelines for contributing to the project

## Project Structure

```
my-app/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API application (10+ endpoints)
│   ├── scraper.py          # Apify scraping logic with mock fallback
│   ├── database.py         # JSON file-based storage layer
│   └── requirements.txt    # Python dependencies
├── frontend/               # React + Vite + Tailwind frontend
│   ├── src/
│   │   ├── App.jsx         # Main application component with routing
│   │   ├── components/     # Reusable UI components
│   │   │   ├── SidebarNav.jsx      # Left navigation sidebar
│   │   │   ├── SearchForm.jsx      # Scraping search form
│   │   │   ├── ResultsTable.jsx    # Results display table
│   │   │   └── DetailSidebar.jsx   # Lead detail panel
│   │   ├── pages/          # Page components
│   │   │   └── CostPage.jsx        # Cost insights page
│   │   └── main.jsx        # React entry point
│   └── package.json        # Node dependencies
├── config/
│   └── audience.yaml       # Target audience configuration (editable)
├── data/                   # JSON storage for runtime data
│   ├── leads.json          # Bookmarked leads
│   └── history.json        # Search history
├── docs/                   # Complete documentation
│   ├── SETUP.md            # Setup and installation guide
│   ├── API.md              # API reference
│   ├── ARCHITECTURE.md     # System architecture
│   ├── DEPLOYMENT.md       # Deployment guide
│   └── COST_ESTIMATION.md  # Cost analysis
├── .env                    # Environment variables (create from .env.example)
├── .env.example            # Example environment configuration
├── init.sh                 # Automated setup script
├── CONTRIBUTING.md         # Contribution guidelines
└── README.md               # This file
```

## Development

### Running in Development Mode

Both frontend and backend support hot reload:

```bash
# Backend (in backend/ directory)
uvicorn main:app --reload

# Frontend (in frontend/ directory)
npm run dev
```

### Building for Production

```bash
# Frontend production build
cd frontend
npm run build
# Build output in frontend/dist/

# Serve production build
npm run preview
```

### Adding New Features

1. Update `config/audience.yaml` for new targeting parameters
2. Add backend endpoints in `backend/main.py`
3. Update frontend components in `frontend/src/`
4. Test using Playwright or manual testing
5. Update documentation

## Cost Insights

See `docs/COST_ESTIMATION.md` for detailed cost analysis including:

- Apify scraping costs (per lead)
- Proxy costs (residential vs datacenter)
- API integration costs (LinkedIn, Twitter, Telegram, TikTok)
- AI enrichment costs (GPT-4, Claude)
- Infrastructure costs (hosting, database)
- Total cost breakdown by scale (1k, 10k, 50k leads/month)
- ROI analysis and revenue potential

**Quick summary:**
- **Small scale (1k-5k leads/month):** $41-$150/month
- **Medium scale (10k-25k leads/month):** $240-$650/month
- **Large scale (50k-100k leads/month):** $1,175-$2,450/month

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│          Frontend (React + Vite + Tailwind)         │
│                http://localhost:5173                 │
│  ┌──────────┐  ┌────────────────┐  ┌─────────────┐ │
│  │ Sidebar  │  │ Search + Table │  │   Detail    │ │
│  │   Nav    │  │    (Results)   │  │   Panel     │ │
│  └──────────┘  └────────────────┘  └─────────────┘ │
└──────────────────────┬──────────────────────────────┘
                       │ REST API (HTTP/JSON)
┌──────────────────────▼──────────────────────────────┐
│           Backend (FastAPI + Python 3.9+)            │
│                http://localhost:8000                 │
│  ┌────────────┐  ┌──────────┐  ┌─────────────────┐ │
│  │ REST API   │  │ Scraper  │  │   Database      │ │
│  │ Endpoints  │  │ (Apify)  │  │ (JSON Files)    │ │
│  └────────────┘  └──────────┘  └─────────────────┘ │
└──────────────────────┬──────────────────────────────┘
                       │ Apify API
┌──────────────────────▼──────────────────────────────┐
│              Apify (Google Maps Scraper)             │
└─────────────────────────────────────────────────────┘
```

**Data Flow:**
1. User submits search via frontend form
2. Frontend sends POST request to `/scrape` endpoint
3. Backend calls Apify API with search parameters
4. Apify scrapes Google Maps and returns business data
5. Backend stores results and returns to frontend
6. Frontend displays results in table
7. User can bookmark leads, export CSV, view history

**See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.**

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Commit message conventions
- Pull request process
- How to add new features

Quick start for contributors:
```bash
# Fork and clone the repo
git clone https://github.com/your-username/my-app.git

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git commit -m "feat: Add new feature"

# Push and create PR
git push origin feature/your-feature-name
```

## License

MIT License - see LICENSE file for details.

## Support and Documentation

- **Setup Help:** [docs/SETUP.md](docs/SETUP.md)
- **API Reference:** [docs/API.md](docs/API.md) or http://localhost:8000/docs
- **Architecture:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Deployment:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Cost Analysis:** [docs/COST_ESTIMATION.md](docs/COST_ESTIMATION.md)
- **Issues:** Create an issue in the repository
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

## Roadmap

Future enhancements:
- [ ] PostgreSQL database support for scalability
- [ ] User authentication and multi-tenancy
- [ ] LinkedIn/Twitter/Telegram scraping integrations
- [ ] AI-powered lead enrichment (GPT-4, Claude)
- [ ] Email finder integration (Hunter.io, Snov.io)
- [ ] CRM integrations (HubSpot, Salesforce, Pipedrive)
- [ ] Scheduled scraping jobs with cron
- [ ] Webhook notifications for new leads
- [ ] Advanced filtering and search
- [ ] Lead scoring and prioritization
- [ ] Email outreach templates
- [ ] Analytics dashboard

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Vite](https://vitejs.dev/) - Frontend build tool
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Apify](https://apify.com/) - Web scraping platform
- [Lucide React](https://lucide.dev/) - Icon library

---

**Last Updated:** February 2026
**Version:** 1.0.0
**Status:** Production Ready
