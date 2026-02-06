# Architecture Documentation - Outreach Scraping Toolkit

System design and technical architecture overview.

## Table of Contents

- [System Overview](#system-overview)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Data Flow](#data-flow)
- [Component Structure](#component-structure)
- [Key Features](#key-features)

## System Overview

The Outreach Scraping Toolkit is a full-stack web application for lead generation and management. It consists of three main layers:

```
┌─────────────────────────────────────────────────────┐
│                  Frontend (React)                    │
│           http://localhost:5173                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Sidebar   │  │ Results Table│  │   Detail   │ │
│  │     Nav     │  │ + Search Form│  │   Panel    │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP/REST API
┌───────────────────────▼─────────────────────────────┐
│              Backend (FastAPI)                       │
│           http://localhost:8000                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │   API    │  │ Scraper  │  │   Database       │  │
│  │ Endpoints│  │  (Apify) │  │ (JSON Files)     │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
└───────────────────────┬─────────────────────────────┘
                        │ API Calls
┌───────────────────────▼─────────────────────────────┐
│            External Services                         │
│  ┌──────────────────────────────────────────────┐  │
│  │  Apify API (Google Maps Scraper)             │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- **Framework:** FastAPI 0.109.0 (Python 3.9+)
- **Web Server:** Uvicorn with auto-reload
- **HTTP Client:** httpx for API calls
- **Scraping:** Apify Client SDK
- **Config:** PyYAML for audience configuration
- **Environment:** python-dotenv for .env loading

**Frontend:**
- **Framework:** React 18.3.1
- **Build Tool:** Vite 5.3.1
- **Styling:** Tailwind CSS 3.4.3
- **Icons:** Lucide React 0.344.0
- **State:** React hooks (useState, useEffect)

**Data Storage:**
- **Format:** JSON files
- **Location:** `data/` directory
- **Files:** `history.json`, `leads.json`

**External APIs:**
- **Apify:** Google Maps Scraper (compass/crawler-google-places)

## Backend Architecture

### Directory Structure

```
backend/
├── main.py          # FastAPI app + REST endpoints
├── scraper.py       # Apify integration + mock data
├── database.py      # JSON file storage layer
└── requirements.txt # Python dependencies
```

### Core Modules

#### 1. main.py (FastAPI Application)

**Responsibilities:**
- Define REST API endpoints
- Handle HTTP requests/responses
- CORS middleware configuration
- Request validation with Pydantic
- Error handling

**Key Features:**
- Auto-generated API documentation (Swagger/ReDoc)
- Pydantic models for type safety
- Async endpoint support
- Graceful error responses

**Endpoints:**
```python
GET  /                          # Health check
GET  /api/config/audience       # Get audience config
POST /scrape                    # Execute scraping
GET  /results                   # Get current results
GET  /history                   # Get search history
POST /history                   # Add to history
GET  /leads                     # Get bookmarks
POST /leads                     # Save bookmark
DELETE /leads/{lead_id}         # Delete bookmark
GET  /download-csv              # Export CSV
GET  /api/cost-analysis         # Get cost data
```

#### 2. scraper.py (Apify Integration)

**Responsibilities:**
- Interface with Apify API
- Handle Google Maps scraping
- Generate mock data for development
- Transform Apify results to application schema

**Workflow:**
```python
1. Check for APIFY_API_TOKEN
2. If token exists:
   a. Initialize ApifyClient
   b. Call Google Maps Scraper actor
   c. Wait for completion
   d. Fetch and transform results
3. If no token or error:
   a. Fall back to mock data generator
4. Return standardized results
```

**Result Schema:**
```python
{
  "id": str,              # Unique identifier
  "name": str,            # Business/company name
  "role": str,            # Contact role (empty for businesses)
  "company": str,         # Company name
  "platform": str,        # "Google Maps"
  "contact_link": str,    # Maps URL
  "region": str,          # City, State
  "notes": str,           # Search keyword
  "rating": float,        # Google rating
  "review_count": int,    # Number of reviews
  "address": str,         # Full address
  "phone": str,           # Phone number
  "website": str,         # Website URL
  "place_id": str         # Google Place ID
}
```

#### 3. database.py (Data Persistence)

**Responsibilities:**
- File-based JSON storage
- In-memory caching for performance
- CRUD operations for history and leads
- Auto-initialization on startup

**Storage Locations:**
```
data/
├── history.json    # Search history
└── leads.json      # Bookmarked leads
```

**In-Memory State:**
- `_history`: List of search history entries
- `_leads`: List of saved leads
- `_current_results`: Latest scraping results (not persisted)

**Operations:**
```python
# History
get_history() -> List[Dict]
add_history(params: Dict) -> Dict

# Leads
get_leads() -> List[Dict]
add_lead(lead_data: Dict) -> Dict
delete_lead(lead_id: str) -> bool

# Current Results
set_current_results(results: List[Dict])
get_current_results() -> List[Dict]
```

### Configuration

#### Environment Variables (.env)

```bash
APIFY_API_TOKEN=xxx  # Required for real scraping
```

#### Audience Configuration (config/audience.yaml)

```yaml
industries: [AI, Web3, blockchain, tech startups]
roles: [Founders, CEOs, Co-founders, BD heads]
regions: [Germany, broader EU, South Asia, Southeast Asia]
platforms: [LinkedIn, X, Telegram, TikTok]
```

**Usage:**
- Loaded via `/api/config/audience` endpoint
- Frontend displays in targeting UI
- Future: Filter scraping results by these criteria

## Frontend Architecture

### Directory Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main app component + routing
│   ├── main.jsx             # React entry point
│   ├── components/
│   │   ├── SidebarNav.jsx   # Left navigation sidebar
│   │   ├── SearchForm.jsx   # Scraping form
│   │   ├── ResultsTable.jsx # Results display table
│   │   └── DetailSidebar.jsx# Lead detail panel
│   └── pages/
│       └── CostPage.jsx     # Cost insights page
├── public/                  # Static assets
├── index.html               # HTML entry point
├── package.json             # Dependencies
├── vite.config.js           # Vite configuration
└── tailwind.config.js       # Tailwind CSS config
```

### Component Hierarchy

```
App.jsx
├── SidebarNav (always visible)
└── Router
    ├── Home Page
    │   ├── SearchForm
    │   ├── ResultsTable
    │   └── DetailSidebar (conditional)
    └── CostPage
        └── Cost analysis sections
```

### Key Components

#### 1. App.jsx (Main Container)

**Responsibilities:**
- Application routing (Home vs Cost Insights)
- Layout structure (3-column design)
- Global state management
- API communication

**State:**
```javascript
const [results, setResults] = useState([])
const [selectedLead, setSelectedLead] = useState(null)
const [view, setView] = useState('home') // 'home' or 'cost'
const [loading, setLoading] = useState(false)
```

**API Calls:**
- Fetch results
- Scrape leads
- Save/delete bookmarks
- Export CSV

#### 2. SidebarNav.jsx (Navigation)

**Responsibilities:**
- Navigation between views
- Visual state management
- Action buttons (Export CSV)

**Features:**
- Dark theme styling
- Active state highlighting
- Icon integration (Lucide React)

#### 3. SearchForm.jsx (Scraping Interface)

**Responsibilities:**
- Collect scraping parameters
- Validate input
- Submit scraping requests
- Display loading state

**Form Fields:**
```javascript
{
  keyword: string,      // Required
  city: string,         // Required
  state: string,        // Required
  max_results: number   // Default: 20
}
```

#### 4. ResultsTable.jsx (Results Display)

**Responsibilities:**
- Display scraping results in table format
- Handle row selection
- Show result metadata (count, source)

**Columns:**
- Name
- Rating
- Review Count
- Address
- Phone
- Website

**Features:**
- Click to select lead
- Highlight selected row
- Responsive design

#### 5. DetailSidebar.jsx (Lead Details)

**Responsibilities:**
- Show full lead details
- Bookmark/unbookmark functionality
- Display all lead fields

**Features:**
- Slide-in panel on the right
- Bookmark button with visual feedback
- All contact information displayed
- Close button

#### 6. CostPage.jsx (Cost Analysis)

**Responsibilities:**
- Fetch cost estimation data from API
- Render markdown content
- Display tables and formatted text

**Features:**
- Parse structured JSON from backend
- Render tables, lists, paragraphs
- Markdown-style formatting

### Styling

**Approach:** Tailwind CSS utility classes

**Theme:**
- Dark mode color scheme
- Gray scale: 800, 700, 600
- Accent: Blue (500, 600)
- Text: White, gray-300, gray-400

**Responsive Design:**
- Desktop-first approach
- 3-column layout on large screens
- Collapsible panels on mobile (future)

## Data Flow

### Scraping Operation Flow

```
1. User fills SearchForm
   ↓
2. App.jsx calls POST /scrape
   ↓
3. Backend scraper.py:
   a. Checks APIFY_API_TOKEN
   b. Calls Apify API or generates mock data
   c. Returns results
   ↓
4. Backend main.py:
   a. Stores results in _current_results
   b. Adds entry to history
   c. Returns results to frontend
   ↓
5. App.jsx updates state
   ↓
6. ResultsTable renders new data
```

### Bookmark Flow

```
1. User clicks lead in ResultsTable
   ↓
2. App.jsx sets selectedLead state
   ↓
3. DetailSidebar displays lead details
   ↓
4. User clicks "Bookmark" button
   ↓
5. App.jsx calls POST /leads
   ↓
6. Backend database.py:
   a. Adds lead to _leads list
   b. Saves to data/leads.json
   c. Returns success
   ↓
7. Frontend shows confirmation
```

### CSV Export Flow

```
1. User clicks "Export CSV" in SidebarNav
   ↓
2. Browser calls GET /download-csv
   ↓
3. Backend main.py:
   a. Fetches _current_results
   b. Converts to CSV format
   c. Streams as file download
   ↓
4. Browser downloads leads.csv
```

## Key Features

### 1. Target Audience Configuration System

**Purpose:** Define targeting parameters for lead generation

**Components:**
- YAML configuration file (`config/audience.yaml`)
- Backend endpoint (`/api/config/audience`)
- Editable configuration (modify YAML directly)

**Usage:**
- Frontend can fetch and display targeting options
- Future: Filter scraping results by audience criteria
- Future: Pre-fill search forms based on audience

### 2. Web Scraping with Apify

**Purpose:** Extract business data from Google Maps

**Features:**
- Real scraping via Apify API
- Graceful fallback to mock data
- Configurable max results
- Standardized output format

**Apify Actor:** `compass/crawler-google-places`

**Input:**
```javascript
{
  searchStringsArray: ["AI startups in Berlin, Germany"],
  maxCrawledPlacesPerSearch: 20,
  language: "en",
  includeWebResults: true,
  scrapeReviews: false
}
```

### 3. Cost Estimation Tool

**Purpose:** Provide cost analysis for scraping operations

**Components:**
- Markdown documentation (`docs/COST_ESTIMATION.md`)
- Parser endpoint (`/api/cost-analysis`)
- Frontend renderer (`CostPage.jsx`)

**Features:**
- Detailed cost breakdown by component
- Pricing at different scales (1k, 10k, 50k leads)
- ROI analysis
- Optimization strategies

### 4. Professional Dashboard UI

**Purpose:** User-friendly interface for lead management

**Layout:**
```
┌──────────────┬────────────────────────────┬──────────────┐
│              │                            │              │
│   Sidebar    │   Search + Results Table   │    Detail    │
│     Nav      │                            │    Panel     │
│              │                            │              │
│  - Home      │  ┌────────────────────┐   │  Lead info   │
│  - History   │  │   Search Form      │   │  when row    │
│  - Bookmarks │  └────────────────────┘   │  selected    │
│  - Cost      │                            │              │
│  - Export    │  [Results table]           │  [Bookmark]  │
│              │                            │              │
└──────────────┴────────────────────────────┴──────────────┘
```

**Design Principles:**
- Dark theme for reduced eye strain
- Clear visual hierarchy
- Instant feedback on actions
- Responsive components

## Performance Considerations

### Backend

- **In-memory caching:** Results stored in memory for fast access
- **Async endpoints:** FastAPI async support for concurrent requests
- **Lazy loading:** JSON files loaded on startup, not per request

### Frontend

- **React hooks:** Efficient state management with useState/useEffect
- **Conditional rendering:** Components only render when needed
- **Vite:** Fast build and hot module replacement

### Database

- **File size:** JSON files are small (< 1MB for 1000s of entries)
- **Read performance:** In-memory cache eliminates file I/O
- **Write performance:** Synchronous writes ensure data integrity

## Security Considerations

### Current (Development)

- No authentication required
- CORS allows all origins
- API token in .env file
- JSON files have standard permissions

### Production Recommendations

- Implement JWT authentication
- Restrict CORS to specific domains
- Use environment-specific API tokens
- Migrate to PostgreSQL or MongoDB
- Add rate limiting
- Implement API key validation
- Encrypt sensitive data
- Use HTTPS only

## Scalability

### Current Limitations

- JSON file storage (not suitable for high volume)
- In-memory results (lost on restart)
- No caching layer
- Single-server deployment

### Future Improvements

- **Database:** Migrate to PostgreSQL/MongoDB
- **Caching:** Add Redis for session data
- **Queue:** Use Celery for async scraping jobs
- **Storage:** S3 for CSV exports
- **CDN:** CloudFront for frontend assets
- **Load Balancing:** Multiple backend instances
- **Monitoring:** Sentry, DataDog, or similar

## Next Steps

- Read [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
- Review [API.md](./API.md) for endpoint details
- Check [SETUP.md](./SETUP.md) for installation
- See [../CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines
