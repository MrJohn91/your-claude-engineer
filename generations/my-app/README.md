# Outreach Scraping Preparation Toolkit

A professional, full-stack lead generation toolkit for scraping and managing outreach contacts from multiple social platforms. Built with a modern web interface, robust backend API, and comprehensive cost analysis tools.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Node](https://img.shields.io/badge/node-16%2B-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688)
![React](https://img.shields.io/badge/React-18.3-61dafb)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Cost Estimation Tool](#cost-estimation-tool)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **Outreach Scraping Preparation Toolkit** is designed to streamline the process of finding and managing leads across multiple social media platforms. It provides:

- **Multi-platform scraping** via Apify API (LinkedIn, X/Twitter, Instagram, TikTok, Telegram)
- **Intelligent filtering** based on industry, role, region, and platform
- **Professional web UI** with modern SaaS aesthetics
- **Export capabilities** to Google Sheets or CSV
- **Cost estimation tools** for budgeting and planning
- **Complete API backend** with FastAPI for integration and automation

This toolkit is perfect for growth teams, sales development, business development, and outreach specialists who need to efficiently generate and manage high-quality lead lists.

---

## Features

### 1. Target Audience Configuration System
- YAML-based configuration for flexible audience targeting
- Predefined filters for industries (AI, Web3, Blockchain, Tech Startups)
- Role-based filtering (Founders, CEOs, BD Heads, Growth Leads, etc.)
- Geographic targeting (Germany, EU, South Asia, Southeast Asia, China)
- Multi-platform support (LinkedIn, X, Instagram, TikTok, Telegram)

### 2. Data Pipeline & API Backend
- FastAPI backend with RESTful endpoints
- Apify API integration for robust multi-platform scraping
- Structured output schema: Name, Role, Company, Platform, Contact Link, Region, Notes
- Real-time scraping progress tracking
- Pagination and filtering for large datasets

### 3. Professional Web UI Dashboard
- Modern React frontend with Tailwind CSS and shadcn/ui components
- Comprehensive filter panel with multi-select capabilities
- Real-time search and results table
- Sortable columns with pagination
- One-click export to Google Sheets or CSV download
- Loading states and progress indicators
- Light/dark mode support

### 4. Google Sheets Integration
- Direct export to Google Sheets via gspread API
- Automatic sheet creation or append to existing sheets
- Formatted headers and structured data layout
- Shareable sheet URLs for team collaboration

### 5. Cost Estimation Tool
- Python-based cost analysis script and Jupyter notebook
- Detailed breakdown of:
  - Apify/scraping costs (per 1k, 10k, 50k records)
  - Proxy costs (residential vs datacenter)
  - API usage fees (LinkedIn, X, etc.)
  - Optional AI enrichment costs (Claude vs GPT-4)
- CSV and Markdown output formats
- Based on current market rates with cited sources

---

## Tech Stack

**Backend:**
- FastAPI 0.115.0 (Python web framework)
- Uvicorn (ASGI server)
- Apify Client (scraping integration)
- gspread (Google Sheets API)
- Pydantic (data validation)
- PyYAML (configuration management)

**Frontend:**
- React 18.3 (UI framework)
- Vite (build tool)
- Tailwind CSS 4.x (styling)
- TypeScript (type safety)
- React Router (navigation)

**Infrastructure:**
- Google Sheets API (data export)
- Apify API (web scraping)
- Python 3.9+
- Node.js 16+

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

1. **Python 3.9 or higher**
   ```bash
   python3 --version
   ```

2. **Node.js 16 or higher** and npm
   ```bash
   node --version
   npm --version
   ```

3. **Apify API Account** (optional for real scraping)
   - Sign up at [apify.com](https://apify.com)
   - Get your API token from the Apify console

4. **Google Cloud Project** (for Sheets export)
   - Create a project at [console.cloud.google.com](https://console.cloud.google.com)
   - Enable Google Sheets API
   - Create service account credentials (JSON file)
   - See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed instructions

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/outreach-scraping-toolkit.git
cd outreach-scraping-toolkit
```

### 2. Run the Initialization Script

The easiest way to get started is using the provided `init.sh` script:

```bash
chmod +x init.sh
./init.sh
```

This will:
- Check for Python and Node.js installation
- Install backend dependencies (Python packages)
- Install frontend dependencies (npm packages)
- Provide options to run backend, frontend, or both

### 3. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# Apify API Configuration
APIFY_API_KEY=your_apify_api_key_here

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_PATH=./config/google-credentials.json
GOOGLE_SHEETS_ENABLED=true

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend Configuration
FRONTEND_URL=http://localhost:5173
```

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed environment configuration.

### 4. Access the Application

Once both servers are running:

- **Frontend Dashboard:** [http://localhost:5173](http://localhost:5173)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Environment Setup

### Backend Setup (Python)

1. **Create a virtual environment (optional but recommended):**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up Google Sheets credentials:**

Place your Google service account JSON file in the `config/` directory and update the `.env` file with the path.

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed Google Sheets setup instructions.

### Frontend Setup (Node.js)

1. **Navigate to frontend directory:**

```bash
cd frontend
```

2. **Install dependencies:**

```bash
npm install
```

3. **Configure API URL (optional):**

If your backend is running on a different port, create a `.env.local` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
```

---

## Running the Application

### Option 1: Using init.sh (Recommended)

```bash
./init.sh
```

Select an option:
1. **Run both backend and frontend** (in separate processes)
2. **Run backend only** (port 8000)
3. **Run frontend only** (port 5173)
4. **Just install dependencies** (no server startup)
5. **Exit**

The script will automatically install missing dependencies and start the selected services.

### Option 2: Manual Startup

**Start Backend (Terminal 1):**

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Start Frontend (Terminal 2):**

```bash
cd frontend
npm run dev
```

The frontend will typically run on `http://localhost:5173` and the backend on `http://localhost:8000`.

---

## Usage Guide

### 1. Setting Filters and Scraping Leads

1. Open the web interface at [http://localhost:5173](http://localhost:5173)
2. Use the filter panel to configure your search:
   - **Platforms**: Select one or more platforms (LinkedIn, X, Instagram, TikTok, Telegram)
   - **Industries**: Choose target industries (AI, Web3, Blockchain, Tech Startups)
   - **Roles**: Select desired roles (Founder, CEO, Co-founder, BD Head, etc.)
   - **Regions**: Pick geographic regions (Germany, EU, South Asia, Southeast Asia, China)
3. Click **"Run Scrape"** to start the scraping process
4. Monitor progress in real-time
5. View results in the sortable table

### 2. Exporting to Google Sheets

1. After scraping, click the **"Export to Sheet"** button
2. Enter a sheet title (optional) or use the default
3. The system will create a new Google Sheet or append to an existing one
4. A shareable URL will be provided
5. Share the sheet with team members as needed

**Note:** Make sure Google Sheets API is configured correctly (see [SETUP_GUIDE.md](./SETUP_GUIDE.md)).

### 3. Downloading as CSV

1. Click the **"Download CSV"** button in the dashboard
2. A CSV file will be generated with all scraped contacts
3. The file will download automatically to your default downloads folder
4. Filename format: `outreach_contacts_YYYYMMDD_HHMMSS.csv`

### 4. Using the Cost Estimation Tool

The cost estimation tool helps you budget your scraping operations based on expected volume.

**Basic Usage:**

```bash
cd tools
python cost_estimation.py
```

This will generate cost estimates for default volumes (1,000, 10,000, and 50,000 records).

**Custom Volumes:**

```bash
python cost_estimation.py --volumes 5000 15000 30000
```

**Include AI Enrichment Costs:**

```bash
python cost_estimation.py --include-ai
```

**Custom Output Directory:**

```bash
python cost_estimation.py --output-dir ./my_analysis
```

**Output Files:**
- `cost_estimates.csv` - Detailed cost breakdown in CSV format
- `cost_estimates.md` - Formatted Markdown table for documentation

See [COST_ESTIMATION_GUIDE.md](./COST_ESTIMATION_GUIDE.md) for detailed usage and interpretation.

---

## Project Structure

```
outreach-scraping-toolkit/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── scraper.py              # Apify integration and scraping logic
│   ├── sheets.py               # Google Sheets export functionality
│   ├── models.py               # Pydantic data models
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── FilterPanel.tsx
│   │   │   ├── ResultsTable.tsx
│   │   │   └── ...
│   │   ├── pages/
│   │   │   └── Dashboard.tsx   # Main dashboard page
│   │   ├── App.tsx             # Root React component
│   │   └── main.tsx            # React entry point
│   ├── package.json            # Node.js dependencies
│   ├── vite.config.ts          # Vite configuration
│   ├── tailwind.config.js      # Tailwind CSS configuration
│   └── tsconfig.json           # TypeScript configuration
│
├── config/
│   ├── audience.yaml           # Target audience configuration
│   └── google-credentials.json # Google service account key (not in git)
│
├── tools/
│   ├── cost_estimation.py      # Cost analysis script
│   ├── cost_estimation.ipynb   # Jupyter notebook version
│   ├── cost_estimates.csv      # Generated cost data (output)
│   └── cost_estimates.md       # Generated cost report (output)
│
├── screenshots/                # Application screenshots (for docs)
│
├── .env.example                # Environment variables template
├── .env                        # Your actual environment variables (not in git)
├── .gitignore                  # Git ignore rules
├── init.sh                     # Initialization and startup script
├── README.md                   # This file
├── SETUP_GUIDE.md              # Detailed setup instructions
├── API_DOCUMENTATION.md        # API endpoint documentation
└── COST_ESTIMATION_GUIDE.md    # Cost estimation tool guide
```

---

## API Documentation

The backend provides a RESTful API for programmatic access and automation.

### Base URL

```
http://localhost:8000
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/health` | Health check endpoint |
| GET | `/api/config/audience` | Get audience configuration |
| POST | `/api/scrape` | Start a scraping job |
| GET | `/api/results` | Retrieve scraped results |
| POST | `/api/export-sheet` | Export to Google Sheets |
| GET | `/api/download-csv` | Download results as CSV |
| GET | `/api/status/{job_id}` | Check scraping job status |

### Example: Start a Scraping Job

```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["LinkedIn", "X"],
    "industries": ["AI", "Web3"],
    "roles": ["Founder", "CEO"],
    "regions": ["Germany", "Broader EU"]
  }'
```

### Example: Get Results

```bash
curl -X GET "http://localhost:8000/api/results?limit=50&offset=0"
```

For complete API documentation with request/response schemas, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) or visit [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI).

---

## Troubleshooting

### Backend Issues

**Problem: `ModuleNotFoundError` when starting backend**

Solution: Make sure you've installed all dependencies:
```bash
cd backend
pip install -r requirements.txt
```

**Problem: `FileNotFoundError` for Google credentials**

Solution: Verify the path in `.env` matches your actual credentials file:
```bash
GOOGLE_SHEETS_CREDENTIALS_PATH=./config/google-credentials.json
```

**Problem: Backend fails to start on port 8000**

Solution: Check if another process is using port 8000:
```bash
lsof -i :8000  # Find process using port 8000
kill -9 <PID>  # Kill the process
```

Or change the port in `.env`:
```env
BACKEND_PORT=8001
```

### Frontend Issues

**Problem: Frontend won't connect to backend**

Solution: Check that the backend is running and the `VITE_API_URL` is correct:
```bash
# In frontend/.env.local
VITE_API_URL=http://localhost:8000
```

**Problem: `npm install` fails**

Solution: Clear npm cache and try again:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Problem: Frontend shows blank page**

Solution: Check browser console for errors. Common issues:
- Backend is not running
- CORS issues (backend should allow frontend origin)
- Missing environment variables

### Google Sheets Issues

**Problem: `google.auth.exceptions.DefaultCredentialsError`**

Solution: Ensure your Google service account JSON is valid and properly configured:
1. Download fresh credentials from Google Cloud Console
2. Enable Google Sheets API for your project
3. Verify the file path in `.env`

**Problem: `gspread.exceptions.APIError: PERMISSION_DENIED`**

Solution: Share the Google Sheet with your service account email:
1. Open the credentials JSON file
2. Find the `client_email` field
3. Share the target Google Sheet with that email address

### Cost Estimation Tool Issues

**Problem: Script fails with import errors**

Solution: Make sure you're in the correct directory and dependencies are installed:
```bash
cd tools
pip install -r ../backend/requirements.txt
python cost_estimation.py
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow code style** conventions:
   - Python: PEP 8
   - TypeScript/React: ESLint rules defined in project
3. **Add tests** for new features
4. **Update documentation** for API or feature changes
5. **Submit a pull request** with a clear description

### Development Workflow

```bash
# Create a feature branch
git checkout -b feature/my-new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to your fork
git push origin feature/my-new-feature

# Open a pull request on GitHub
```

---

## Architecture Overview

### Backend Architecture

The backend follows a modular architecture:

1. **main.py**: FastAPI application with route definitions
2. **scraper.py**: Apify API integration with mock data fallback
3. **sheets.py**: Google Sheets API integration
4. **models.py**: Pydantic schemas for data validation

**Data Flow:**
```
User Request → FastAPI Endpoint → Scraper Service → Apify API
                                        ↓
                                 Process Results
                                        ↓
                     ← JSON Response ← Store in Memory
```

### Frontend Architecture

The frontend is a single-page React application:

1. **App.tsx**: Root component with routing
2. **Dashboard.tsx**: Main page orchestrating filters and results
3. **FilterPanel.tsx**: Multi-select filters component
4. **ResultsTable.tsx**: Sortable, paginated table component

**State Management:**
- React hooks for local state
- API calls via fetch
- Real-time updates during scraping

---

## Cost Estimates

Based on the cost estimation tool (see [COST_ESTIMATION_GUIDE.md](./COST_ESTIMATION_GUIDE.md)), here are typical costs:

| Volume | Scraping | Proxies (Residential) | API Fees | Total |
|--------|----------|----------------------|----------|-------|
| 1,000 records | $0.50 - $1.00 | $0.10 - $0.25 | $100/mo | ~$100.60 - $101.25 |
| 10,000 records | $4.50 - $9.00 | $1.00 - $2.50 | $100/mo | ~$105.50 - $111.50 |
| 50,000 records | $20.00 - $40.00 | $5.00 - $12.50 | $100/mo | ~$125.00 - $152.50 |

**Notes:**
- Costs are estimates based on current market rates (Jan 2025)
- API fees are monthly subscriptions (e.g., X API Basic tier)
- Residential proxies recommended for better success rates
- Volume discounts may be available from providers

---

## License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Outreach Scraping Toolkit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Support

For issues, questions, or feature requests:

1. **Check the documentation** in this repository
2. **Search existing issues** on GitHub
3. **Open a new issue** with detailed information:
   - Expected behavior
   - Actual behavior
   - Steps to reproduce
   - Environment details (OS, Python version, Node version)

---

## Roadmap

Future enhancements planned:

- [ ] Real-time scraping progress with WebSockets
- [ ] User authentication and multi-user support
- [ ] Job scheduling and automation
- [ ] Advanced filtering and search capabilities
- [ ] Email enrichment and validation
- [ ] CRM integrations (Salesforce, HubSpot)
- [ ] AI-powered lead scoring
- [ ] Analytics dashboard with charts and insights

---

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Apify](https://apify.com/) - Web scraping platform
- [Google Sheets API](https://developers.google.com/sheets/api) - Data export
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

---

**Happy Lead Generation!**

For detailed setup instructions, see [SETUP_GUIDE.md](./SETUP_GUIDE.md).

For API usage details, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md).

For cost analysis, see [COST_ESTIMATION_GUIDE.md](./COST_ESTIMATION_GUIDE.md).
