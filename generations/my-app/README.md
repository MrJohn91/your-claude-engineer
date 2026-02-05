# Outreach Scraping Preparation Toolkit

A complete outreach lead generation toolkit with a polished web UI for scraping and managing leads from multiple social platforms.

## Tech Stack

- **Backend**: FastAPI with REST API endpoints
- **Frontend**: React + Vite + Tailwind CSS + shadcn/ui
- **Database**: Google Sheets via gspread API
- **Scraping**: Apify API integration
- **Configuration**: YAML-based audience targeting

## Features Overview

1. **Target Audience Configuration System** - YAML-based configuration with predefined filters for industries, roles, regions, and platforms
2. **Data Pipeline & API Backend** - Apify API integration for multi-platform contact scraping with REST endpoints
3. **Professional Web UI Dashboard** - Modern SaaS aesthetic with filter panel, results table, and export functionality
4. **Cost Estimation Tool** - Python script analyzing Apify, proxy, and API usage costs
5. **Complete Documentation & Setup** - Comprehensive guides for setup, configuration, and usage

## Project File Structure

```
backend/
├── main.py              - FastAPI application
├── scraper.py           - Apify integration
├── sheets.py            - Google Sheets export
└── requirements.txt     - Python dependencies

frontend/
├── src/
│   ├── components/      - React components
│   ├── pages/          - Main dashboard
│   └── styles/         - Tailwind CSS
├── package.json
└── vite.config.js

config/
└── audience.yaml        - Target audience configuration

tools/
├── cost_estimation.py   - Cost analysis script
└── cost_estimation.ipynb - Jupyter notebook version

.env.example            - Environment variables template
README.md              - Complete setup and usage guide
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- Apify account with API token
- Google Cloud credentials for Sheets API

### Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MrJohn91/Outreach-Scraping-Preparation-Toolkit.git
   cd Outreach-Scraping-Preparation-Toolkit
   ```

2. Run the initialization script:
   ```bash
   chmod +x init.sh
   ./init.sh
   ```

3. Follow the setup guide in `SETUP.md` for detailed environment configuration.

### Running the Application

#### Option 1: Using the init script
```bash
./init.sh
# Select option to run both backend and frontend or individual services
```

#### Option 2: Manual startup

**Backend:**
```bash
cd backend
python -m uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000` (frontend) and `http://localhost:8000` (backend API).

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Apify API Configuration
APIFY_API_TOKEN=your_apify_api_token

# Google Sheets API
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Application
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

Refer to `.env.example` for the complete template.

## Usage

### Scraping Leads

1. Configure target audience in `config/audience.yaml`
2. Use the web UI to select filters (industries, roles, regions, platforms)
3. Click "Run Scrape" to start the scraping process
4. Monitor progress and results in the dashboard

### Exporting Data

- **Google Sheets**: Click "Export to Sheet" to send results directly to Google Sheets
- **CSV Download**: Click "Download CSV" to export results locally

### Cost Analysis

Run the cost estimation tool to analyze project costs:

```bash
python tools/cost_estimation.py
```

See `tools/cost_estimation.ipynb` for interactive analysis.

## Documentation

- [Setup Guide](./SETUP.md) - Detailed environment and dependency setup
- [API Documentation](./backend/API.md) - FastAPI endpoints and schemas
- [Configuration Guide](./config/README.md) - Audience targeting configuration
- [Cost Estimation Guide](./tools/README.md) - Cost analysis tool usage

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue or submit a pull request.
