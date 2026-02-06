# API Documentation - Outreach Scraping Toolkit

Complete REST API reference for the Outreach Scraping Toolkit backend.

## Base URL

```
http://localhost:8000
```

## Authentication

The current version does not require authentication. All endpoints are publicly accessible for development purposes.

**Production Note:** Implement authentication before deploying to production (see [DEPLOYMENT.md](./DEPLOYMENT.md)).

## Interactive Documentation

The API provides interactive documentation via Swagger UI:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These interfaces allow you to test endpoints directly in the browser.

## Endpoints

### Health Check

#### `GET /`

Check if the API is running and get version information.

**Response:**
```json
{
  "status": "ok",
  "message": "Outreach Scraping Toolkit API is running",
  "version": "1.0.0"
}
```

**Example:**
```bash
curl http://localhost:8000/
```

---

### Configuration

#### `GET /api/config/audience`

Get the target audience configuration from the YAML file.

**Response:**
```json
{
  "status": "success",
  "data": {
    "industries": ["AI", "Web3", "blockchain", "tech startups"],
    "roles": ["Founders", "CEOs", "Co-founders", "BD heads"],
    "regions": ["Germany", "broader EU", "South Asia", "Southeast Asia"],
    "platforms": ["LinkedIn", "X", "Telegram", "TikTok"]
  }
}
```

**Example:**
```bash
curl http://localhost:8000/api/config/audience
```

**Status Codes:**
- `200 OK` - Configuration retrieved successfully
- `404 Not Found` - Configuration file doesn't exist
- `500 Internal Server Error` - Error loading configuration

---

### Scraping

#### `POST /scrape`

Execute a web scraping operation to find leads using Apify's Google Maps scraper.

**Request Body:**
```json
{
  "keyword": "AI startups",
  "city": "Berlin",
  "state": "Germany",
  "max_results": 20
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `keyword` | string | Yes | Search keyword (e.g., "AI startups", "blockchain companies") |
| `city` | string | Yes | City or area to search in |
| `state` | string | Yes | State, region, or country |
| `max_results` | integer | No | Maximum results to return (default: 20, max: 100) |

**Response:**
```json
{
  "status": "success",
  "message": "Found 15 results",
  "count": 15,
  "results": [
    {
      "id": "apify_a1b2c3d4",
      "name": "TechHub Berlin",
      "role": "",
      "company": "TechHub Berlin",
      "platform": "Google Maps",
      "contact_link": "https://www.google.com/maps/place/?q=place_id:ChIJ...",
      "region": "Berlin, Germany",
      "notes": "AI startups",
      "rating": 4.7,
      "review_count": 342,
      "address": "123 Tech Street, Berlin, Germany",
      "phone": "+49-30-1234567",
      "website": "https://www.techhubberlin.com",
      "place_id": "ChIJxxxxxxxxx"
    }
  ]
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "AI startups",
    "city": "Berlin",
    "state": "Germany",
    "max_results": 20
  }'
```

**Status Codes:**
- `200 OK` - Scraping completed successfully
- `400 Bad Request` - Missing required parameters
- `500 Internal Server Error` - Scraping failed

**Notes:**
- Falls back to mock data if `APIFY_API_TOKEN` is not configured
- Results are automatically saved to search history
- Results are stored as current results (accessible via `/results`)

---

### Results

#### `GET /results`

Get the current search results from the last scraping operation.

**Response:**
```json
{
  "status": "success",
  "count": 15,
  "results": [
    {
      "id": "apify_a1b2c3d4",
      "name": "TechHub Berlin",
      "rating": 4.7,
      "review_count": 342,
      "address": "123 Tech Street, Berlin, Germany",
      "phone": "+49-30-1234567",
      "website": "https://www.techhubberlin.com",
      "place_id": "ChIJxxxxxxxxx"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/results
```

**Status Codes:**
- `200 OK` - Results retrieved (may be empty array if no scraping done yet)

---

### History Management

#### `GET /history`

Get all search history entries.

**Response:**
```json
{
  "status": "success",
  "count": 5,
  "history": [
    {
      "id": "history_1707234567.123",
      "timestamp": "2026-02-06T15:30:00.000Z",
      "params": {
        "keyword": "AI startups",
        "city": "Berlin",
        "state": "Germany",
        "max_results": 20
      },
      "result_count": 15
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/history
```

**Status Codes:**
- `200 OK` - History retrieved successfully

---

#### `POST /history`

Add a search to history manually (usually done automatically by `/scrape`).

**Request Body:**
```json
{
  "params": {
    "keyword": "Web3 companies",
    "city": "Singapore",
    "state": "Singapore",
    "max_results": 30
  },
  "result_count": 25
}
```

**Response:**
```json
{
  "status": "success",
  "message": "History entry added",
  "entry": {
    "id": "history_1707234567.123",
    "timestamp": "2026-02-06T15:30:00.000Z",
    "params": {
      "keyword": "Web3 companies",
      "city": "Singapore",
      "state": "Singapore",
      "max_results": 30
    },
    "result_count": 25
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/history \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "keyword": "Web3 companies",
      "city": "Singapore",
      "state": "Singapore"
    },
    "result_count": 25
  }'
```

**Status Codes:**
- `200 OK` - History entry added
- `500 Internal Server Error` - Failed to add history

---

### Leads (Bookmarks)

#### `GET /leads`

Get all saved/bookmarked leads.

**Response:**
```json
{
  "status": "success",
  "count": 3,
  "leads": [
    {
      "id": "apify_a1b2c3d4",
      "name": "TechHub Berlin",
      "role": "",
      "company": "TechHub Berlin",
      "platform": "Google Maps",
      "contact_link": "https://www.google.com/maps/place/?q=place_id:ChIJ...",
      "region": "Berlin, Germany",
      "notes": "AI startups",
      "rating": 4.7,
      "review_count": 342,
      "address": "123 Tech Street, Berlin, Germany",
      "phone": "+49-30-1234567",
      "website": "https://www.techhubberlin.com",
      "place_id": "ChIJxxxxxxxxx",
      "saved_at": "2026-02-06T15:30:00.000Z"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/leads
```

**Status Codes:**
- `200 OK` - Leads retrieved successfully

---

#### `POST /leads`

Save a lead to bookmarks.

**Request Body:**
```json
{
  "id": "apify_a1b2c3d4",
  "name": "TechHub Berlin",
  "role": "",
  "company": "TechHub Berlin",
  "platform": "Google Maps",
  "contact_link": "https://www.google.com/maps/place/?q=place_id:ChIJ...",
  "region": "Berlin, Germany",
  "notes": "High priority - follow up next week",
  "rating": 4.7,
  "review_count": 342,
  "address": "123 Tech Street, Berlin, Germany",
  "phone": "+49-30-1234567",
  "website": "https://www.techhubberlin.com",
  "place_id": "ChIJxxxxxxxxx"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the lead |
| `name` | string | Yes | Lead/company name |
| `role` | string | No | Contact's role/title |
| `company` | string | No | Company name |
| `platform` | string | No | Platform where lead was found |
| `contact_link` | string | No | URL to contact/profile |
| `region` | string | No | Geographic region |
| `notes` | string | No | Custom notes about the lead |
| `rating` | float | No | Rating (if applicable) |
| `review_count` | integer | No | Number of reviews |
| `address` | string | No | Physical address |
| `phone` | string | No | Phone number |
| `website` | string | No | Website URL |
| `place_id` | string | No | Google Maps place ID |

**Response:**
```json
{
  "status": "success",
  "message": "Lead saved successfully",
  "lead": {
    "id": "apify_a1b2c3d4",
    "name": "TechHub Berlin",
    "saved_at": "2026-02-06T15:30:00.000Z"
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/leads \
  -H "Content-Type: application/json" \
  -d '{
    "id": "apify_a1b2c3d4",
    "name": "TechHub Berlin",
    "company": "TechHub Berlin",
    "platform": "Google Maps",
    "region": "Berlin, Germany",
    "notes": "High priority contact"
  }'
```

**Status Codes:**
- `200 OK` - Lead saved successfully
- `500 Internal Server Error` - Failed to save lead

**Notes:**
- Duplicate leads (same `id`) will not be saved again
- `saved_at` timestamp is automatically added

---

#### `DELETE /leads/{lead_id}`

Remove a lead from bookmarks.

**URL Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `lead_id` | string | The unique ID of the lead to delete |

**Response:**
```json
{
  "status": "success",
  "message": "Lead deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/leads/apify_a1b2c3d4
```

**Status Codes:**
- `200 OK` - Lead deleted successfully
- `404 Not Found` - Lead not found
- `500 Internal Server Error` - Failed to delete lead

---

### Export

#### `GET /download-csv`

Export current search results to CSV format.

**Response:**
- Content-Type: `text/csv`
- File download with name `leads.csv`

**CSV Columns:**
- `id` - Unique identifier
- `name` - Lead/company name
- `role` - Contact role
- `company` - Company name
- `platform` - Source platform
- `contact_link` - Contact URL
- `region` - Geographic region
- `notes` - Notes
- `rating` - Rating score
- `review_count` - Number of reviews
- `address` - Physical address
- `phone` - Phone number
- `website` - Website URL
- `place_id` - Google Maps ID

**Example:**
```bash
curl http://localhost:8000/download-csv -o leads.csv
```

**Status Codes:**
- `200 OK` - CSV file downloaded successfully
- `404 Not Found` - No results to download
- `500 Internal Server Error` - Failed to generate CSV

**Notes:**
- Only exports current results (from latest `/scrape` call)
- Empty fields are included as empty strings
- Compatible with Excel, Google Sheets, and all CSV readers

---

### Cost Analysis

#### `GET /api/cost-analysis`

Get parsed cost estimation data from the markdown documentation.

**Response:**
```json
{
  "status": "success",
  "data": {
    "title": "Cost Estimation - Outreach Scraping Toolkit",
    "sections": [
      {
        "type": "section",
        "level": 2,
        "title": "Cost Breakdown by Component",
        "content": [
          {
            "type": "table",
            "headers": ["Component", "Cost per Lead", "Monthly at 10k Leads"],
            "rows": [
              ["Apify Scraping", "$0.01", "$100"],
              ["Proxies", "$0.005", "$50"]
            ]
          }
        ]
      }
    ]
  }
}
```

**Example:**
```bash
curl http://localhost:8000/api/cost-analysis
```

**Status Codes:**
- `200 OK` - Cost analysis retrieved
- `404 Not Found` - Cost estimation document not found
- `500 Internal Server Error` - Failed to parse document

**Notes:**
- Parses `docs/COST_ESTIMATION.md` into structured JSON
- Used by frontend Cost Insights page
- Includes tables, lists, and formatted text

---

## Error Handling

All endpoints return errors in a consistent format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid input parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server-side error

## Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider adding rate limiting middleware.

## CORS

The API allows all origins in development mode. Update CORS settings in `backend/main.py` for production.

## Data Persistence

- **History:** Stored in `data/history.json`
- **Bookmarks:** Stored in `data/leads.json`
- **Current Results:** In-memory only (lost on restart)

## Next Steps

- Read [SETUP.md](./SETUP.md) for installation instructions
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
