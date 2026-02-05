# API Documentation - Outreach Scraping Toolkit

Complete API reference for the Outreach Scraping Toolkit backend.

## Base URL

```
http://localhost:8000
```

For production, replace with your deployed backend URL.

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints Overview](#endpoints-overview)
3. [Root & Health Endpoints](#root--health-endpoints)
4. [Configuration Endpoints](#configuration-endpoints)
5. [Scraping Endpoints](#scraping-endpoints)
6. [Results Endpoints](#results-endpoints)
7. [Export Endpoints](#export-endpoints)
8. [Data Models](#data-models)
9. [Error Handling](#error-handling)
10. [Rate Limiting](#rate-limiting)
11. [Testing with cURL](#testing-with-curl)

---

## Authentication

**Current Version:** No authentication required.

For production deployments, consider adding:
- API key authentication
- JWT tokens
- OAuth 2.0

Example future header:
```
Authorization: Bearer your_api_token_here
```

---

## Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Root endpoint with API info | No |
| GET | `/health` | Health check | No |
| GET | `/api/config/audience` | Get audience configuration | No |
| POST | `/api/scrape` | Start scraping job | No |
| GET | `/api/results` | Get scraped results | No |
| POST | `/api/export-sheet` | Export to Google Sheets | No |
| GET | `/api/download-csv` | Download CSV file | No |
| GET | `/api/status/{job_id}` | Get job status | No |

---

## Root & Health Endpoints

### GET `/`

Root endpoint providing API information.

**Request:**
```bash
curl http://localhost:8000/
```

**Response:** `200 OK`

```json
{
  "message": "Outreach Scraping Toolkit API",
  "version": "1.0.0",
  "endpoints": {
    "config": "/api/config/audience",
    "scrape": "/api/scrape",
    "results": "/api/results",
    "export": "/api/export-sheet",
    "download": "/api/download-csv"
  }
}
```

---

### GET `/health`

Health check endpoint for monitoring.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:** `200 OK`

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

**Response Fields:**
- `status`: `"healthy"` or `"unhealthy"`
- `timestamp`: ISO 8601 formatted timestamp
- `services.scraper`: Boolean indicating scraper service status
- `services.sheets`: Boolean indicating Google Sheets service status

---

## Configuration Endpoints

### GET `/api/config/audience`

Retrieve the target audience configuration including available platforms, industries, roles, and regions.

**Request:**
```bash
curl http://localhost:8000/api/config/audience
```

**Response:** `200 OK`

```json
{
  "platforms": [
    "LinkedIn",
    "X",
    "Telegram",
    "TikTok",
    "Instagram"
  ],
  "industries": [
    "AI",
    "Web3",
    "Blockchain",
    "Tech Startups"
  ],
  "roles": [
    "Founder",
    "CEO",
    "Co-founder",
    "BD Head",
    "Product Owner",
    "Growth Lead"
  ],
  "regions": [
    "Germany",
    "Broader EU",
    "Other European Countries",
    "South Asia",
    "Southeast Asia",
    "China"
  ]
}
```

**Use Case:**
- Populate filter dropdowns in the frontend
- Validate filter selections before scraping
- Display available options to users

**Error Responses:**

`500 Internal Server Error` - Configuration file not loaded
```json
{
  "detail": "Audience configuration not loaded"
}
```

---

## Scraping Endpoints

### POST `/api/scrape`

Start a scraping job with specified filters.

**Request:**

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

**Request Body Schema:**

```json
{
  "platforms": ["string"],      // Required: At least one platform
  "industries": ["string"],     // Optional: Filter by industry
  "roles": ["string"],          // Optional: Filter by role
  "regions": ["string"],        // Optional: Filter by region
  "search_query": "string"      // Optional: Additional search terms
}
```

**Example Request Body:**

```json
{
  "platforms": ["LinkedIn", "Instagram"],
  "industries": ["AI", "Blockchain"],
  "roles": ["Founder", "Co-founder", "CEO"],
  "regions": ["Germany", "South Asia"],
  "search_query": "machine learning startup"
}
```

**Response:** `200 OK`

```json
{
  "status": "success",
  "message": "Successfully scraped 45 contacts from 2 platform(s)",
  "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "total_results": 45
}
```

**Response Fields:**
- `status`: `"success"` or `"error"`
- `message`: Human-readable status message
- `job_id`: Unique identifier for the scraping job
- `total_results`: Number of contacts found

**Error Responses:**

`400 Bad Request` - Invalid parameters
```json
{
  "detail": "At least one platform must be specified"
}
```

`503 Service Unavailable` - Scraper not initialized
```json
{
  "detail": "Scraper service not initialized"
}
```

`500 Internal Server Error` - Scraping failed
```json
{
  "detail": "Scraping failed: [error details]"
}
```

---

### GET `/api/status/{job_id}`

Check the status of a scraping job.

**Request:**
```bash
curl http://localhost:8000/api/status/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Path Parameters:**
- `job_id`: UUID of the scraping job (from POST /api/scrape response)

**Response:** `200 OK`

```json
{
  "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "completed",
  "progress": 100,
  "total_results": 45,
  "started_at": "2026-02-05T10:30:00.123456",
  "completed_at": "2026-02-05T10:32:15.789012"
}
```

**Status Values:**
- `pending`: Job queued but not started
- `running`: Scraping in progress
- `completed`: Job finished successfully
- `failed`: Job encountered an error
- `cancelled`: Job was cancelled by user

---

## Results Endpoints

### GET `/api/results`

Retrieve scraped contact results with pagination.

**Request:**
```bash
curl "http://localhost:8000/api/results?limit=50&offset=0"
```

**Query Parameters:**
- `limit` (optional): Number of results per page (default: 50, max: 500)
- `offset` (optional): Number of results to skip (default: 0)

**Response:** `200 OK`

```json
{
  "total": 145,
  "limit": 50,
  "offset": 0,
  "data": [
    {
      "name": "John Doe",
      "role": "Founder & CEO",
      "company": "AI Startup Inc",
      "platform": "LinkedIn",
      "contact_link": "https://linkedin.com/in/johndoe",
      "region": "Germany",
      "notes": "Berlin-based AI startup, Series A funded"
    },
    {
      "name": "Jane Smith",
      "role": "Co-founder",
      "company": "Web3 Solutions",
      "platform": "X",
      "contact_link": "https://x.com/janesmith",
      "region": "Broader EU",
      "notes": "Amsterdam-based Web3 company"
    }
    // ... more results
  ]
}
```

**Response Fields:**
- `total`: Total number of results available
- `limit`: Number of results returned in this response
- `offset`: Starting position of this page
- `data`: Array of contact objects (see [Contact Schema](#contact-schema))

**Pagination Example:**

```bash
# Page 1 (results 0-49)
curl "http://localhost:8000/api/results?limit=50&offset=0"

# Page 2 (results 50-99)
curl "http://localhost:8000/api/results?limit=50&offset=50"

# Page 3 (results 100-149)
curl "http://localhost:8000/api/results?limit=50&offset=100"
```

**Error Responses:**

`503 Service Unavailable` - Scraper not initialized
```json
{
  "detail": "Scraper service not initialized"
}
```

`500 Internal Server Error` - Failed to retrieve results
```json
{
  "detail": "Failed to retrieve results: [error details]"
}
```

---

## Export Endpoints

### POST `/api/export-sheet`

Export scraped results to Google Sheets.

**Request:**

```bash
curl -X POST http://localhost:8000/api/export-sheet \
  -H "Content-Type: application/json" \
  -d '{
    "sheet_title": "Outreach Contacts - Feb 2026",
    "include_notes": true
  }'
```

**Request Body Schema:**

```json
{
  "sheet_id": "string",           // Optional: Existing sheet ID to append to
  "sheet_title": "string",        // Optional: Title for new sheet
  "include_notes": boolean        // Optional: Include notes column (default: true)
}
```

**Response:** `200 OK`

```json
{
  "status": "success",
  "message": "Successfully exported 145 contacts to Google Sheets",
  "sheet_url": "https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j/edit",
  "sheet_id": "1a2b3c4d5e6f7g8h9i0j"
}
```

**Response Fields:**
- `status`: `"success"` or `"error"`
- `message`: Human-readable status message
- `sheet_url`: Direct link to the Google Sheet
- `sheet_id`: Google Sheet ID (for future appends)

**Error Responses:**

`400 Bad Request` - No data to export
```json
{
  "detail": "No data available to export. Please run a scrape first."
}
```

`503 Service Unavailable` - Service not initialized
```json
{
  "detail": "Google Sheets service not initialized"
}
```

`500 Internal Server Error` - Export failed
```json
{
  "detail": "Export to Google Sheets failed: [error details]"
}
```

---

### GET `/api/download-csv`

Download scraped results as a CSV file.

**Request:**

```bash
curl -O -J "http://localhost:8000/api/download-csv?filename=my_contacts.csv"
```

**Query Parameters:**
- `filename` (optional): Custom filename for the CSV (default: auto-generated with timestamp)

**Response:** `200 OK`

**Response Headers:**
```
Content-Type: text/csv
Content-Disposition: attachment; filename=outreach_contacts_20260205_103000.csv
```

**CSV Format:**

```csv
Name,Role,Company,Platform,Contact Link,Region,Notes
John Doe,Founder & CEO,AI Startup Inc,LinkedIn,https://linkedin.com/in/johndoe,Germany,Berlin-based AI startup
Jane Smith,Co-founder,Web3 Solutions,X,https://x.com/janesmith,Broader EU,Amsterdam-based Web3 company
```

**Error Responses:**

`400 Bad Request` - No data to download
```json
{
  "detail": "No data available to download. Please run a scrape first."
}
```

`503 Service Unavailable` - Service not initialized
```json
{
  "detail": "Scraper service not initialized"
}
```

`500 Internal Server Error` - Download failed
```json
{
  "detail": "CSV download failed: [error details]"
}
```

---

## Data Models

### Contact Schema

The core data model for scraped contacts.

```typescript
{
  name: string;              // Full name
  role: string;              // Job title or role
  company: string;           // Company name
  platform: Platform;        // Source platform (enum)
  contact_link: string;      // Profile URL
  region: string;            // Geographic region
  notes?: string;            // Optional additional information
}
```

**Platform Enum:**
- `"LinkedIn"`
- `"X"`
- `"Instagram"`
- `"TikTok"`
- `"Telegram"`

**Example:**

```json
{
  "name": "Alice Johnson",
  "role": "Growth Lead",
  "company": "Blockchain Ventures",
  "platform": "LinkedIn",
  "contact_link": "https://linkedin.com/in/alicejohnson",
  "region": "Southeast Asia",
  "notes": "Singapore-based, 5+ years in growth marketing"
}
```

---

### Scrape Request Schema

```typescript
{
  platforms: string[];       // Required: At least one platform
  industries?: string[];     // Optional: Industry filters
  roles?: string[];          // Optional: Role filters
  regions?: string[];        // Optional: Region filters
  search_query?: string;     // Optional: Additional search terms
}
```

---

### Scrape Response Schema

```typescript
{
  status: "success" | "error";
  message: string;
  job_id: string;            // UUID format
  total_results: number;
}
```

---

### Results Response Schema

```typescript
{
  total: number;             // Total available results
  limit: number;             // Results in this response
  offset: number;            // Starting position
  data: Contact[];           // Array of contacts
}
```

---

### Export Sheet Request Schema

```typescript
{
  sheet_id?: string;         // Optional: Existing sheet ID
  sheet_title?: string;      // Optional: New sheet title
  include_notes?: boolean;   // Optional: Include notes column
}
```

---

### Export Sheet Response Schema

```typescript
{
  status: "success" | "error";
  message: string;
  sheet_url: string;         // Google Sheets URL
  sheet_id: string;          // Google Sheets ID
}
```

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid parameters, missing required fields |
| 404 | Not Found | Endpoint or resource doesn't exist |
| 500 | Internal Server Error | Server-side error, scraping failed |
| 503 | Service Unavailable | Service not initialized or unavailable |

### Common Error Scenarios

**1. No Platforms Specified**

Request:
```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"industries": ["AI"]}'
```

Response: `400 Bad Request`
```json
{
  "detail": "At least one platform must be specified"
}
```

**2. Invalid JSON**

Request:
```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{invalid json}'
```

Response: `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "loc": ["body"],
      "msg": "Expecting property name enclosed in double quotes",
      "type": "value_error.jsondecode"
    }
  ]
}
```

**3. Service Not Initialized**

Request:
```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["LinkedIn"]}'
```

Response: `503 Service Unavailable`
```json
{
  "detail": "Scraper service not initialized"
}
```

---

## Rate Limiting

**Current Version:** No rate limiting enforced.

**Recommendations for Production:**

Implement rate limiting to prevent abuse:

```python
# Example: 100 requests per minute per IP
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/scrape")
@limiter.limit("10/minute")
async def scrape_contacts(request: Request, ...):
    # ...
```

**Suggested Limits:**
- `/api/scrape`: 10 requests/minute
- `/api/results`: 60 requests/minute
- `/api/export-sheet`: 5 requests/minute
- Other endpoints: 120 requests/minute

---

## Testing with cURL

### Complete Testing Workflow

**1. Check Health:**

```bash
curl http://localhost:8000/health
```

**2. Get Configuration:**

```bash
curl http://localhost:8000/api/config/audience
```

**3. Start Scraping:**

```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["LinkedIn", "X"],
    "industries": ["AI", "Web3"],
    "roles": ["Founder", "CEO"],
    "regions": ["Germany"]
  }'
```

**4. Get Results (first page):**

```bash
curl "http://localhost:8000/api/results?limit=10&offset=0"
```

**5. Export to Google Sheets:**

```bash
curl -X POST http://localhost:8000/api/export-sheet \
  -H "Content-Type: application/json" \
  -d '{
    "sheet_title": "Test Export",
    "include_notes": true
  }'
```

**6. Download CSV:**

```bash
curl -O -J "http://localhost:8000/api/download-csv?filename=test_export.csv"
```

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

### Swagger UI

Access at: [http://localhost:8000/docs](http://localhost:8000/docs)

Features:
- Try out endpoints directly in the browser
- See request/response schemas
- View example requests and responses
- No authentication needed

### ReDoc

Access at: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Features:
- Clean, readable documentation
- Searchable endpoint list
- Detailed schema definitions
- Export to PDF

---

## Postman Collection

Import this JSON to use with Postman:

```json
{
  "info": {
    "name": "Outreach Scraping Toolkit API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/health",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["health"]
        }
      }
    },
    {
      "name": "Get Audience Config",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/config/audience",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "config", "audience"]
        }
      }
    },
    {
      "name": "Start Scraping",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"platforms\": [\"LinkedIn\"],\n  \"industries\": [\"AI\"],\n  \"roles\": [\"Founder\"],\n  \"regions\": [\"Germany\"]\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/scrape",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "scrape"]
        }
      }
    }
  ]
}
```

---

## Support & Feedback

For API questions or feature requests:

1. Check [GitHub Issues](https://github.com/your-username/outreach-scraping-toolkit/issues)
2. Review [README.md](./README.md) troubleshooting section
3. Open a new issue with:
   - API endpoint affected
   - Request details
   - Expected vs actual response
   - Error messages

---

**API Version:** 1.0.0
**Last Updated:** 2026-02-05
