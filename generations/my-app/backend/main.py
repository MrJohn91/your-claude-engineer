"""
FastAPI Backend for Outreach Scraping Toolkit
Provides REST API endpoints for lead generation and management.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
import io
import csv
import re

from scraper import scrape_google_maps
import database as db

# Load environment variables from project root (parent of backend/)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

# Initialize FastAPI app
app = FastAPI(
    title="Outreach Scraping Toolkit API",
    description="API for lead generation and management",
    version="1.0.0"
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to config file
CONFIG_PATH = Path(__file__).parent.parent / "config" / "audience.yaml"


# Pydantic Models
class ScrapeRequest(BaseModel):
    keyword: str
    city: str
    state: str
    max_results: int = 20


class HistoryRequest(BaseModel):
    params: Dict
    result_count: int = 0


class LeadRequest(BaseModel):
    id: str
    name: str
    role: Optional[str] = ""
    company: Optional[str] = ""
    platform: Optional[str] = "Google Maps"
    contact_link: Optional[str] = ""
    region: Optional[str] = ""
    notes: Optional[str] = ""
    rating: Optional[float] = 0
    review_count: Optional[int] = 0
    address: Optional[str] = ""
    phone: Optional[str] = ""
    website: Optional[str] = ""
    place_id: Optional[str] = ""


# Health Check Endpoint
@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Outreach Scraping Toolkit API is running",
        "version": "1.0.0"
    }


# Configuration Endpoint
@app.get("/api/config/audience")
async def get_audience_config():
    """Get the audience configuration from YAML file."""
    try:
        if not CONFIG_PATH.exists():
            raise HTTPException(status_code=404, detail="Configuration file not found")

        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)

        return {
            "status": "success",
            "data": config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading configuration: {str(e)}")


# Scraping Endpoint
@app.post("/scrape")
async def scrape_leads(request: ScrapeRequest):
    """
    Scrape leads using Apify Google Maps scraper.
    Falls back to mock data if APIFY_API_TOKEN is not configured.
    """
    try:
        # Validate inputs
        if not request.keyword or not request.city or not request.state:
            raise HTTPException(status_code=400, detail="Missing required parameters")

        # Run scraper
        results = scrape_google_maps(
            keyword=request.keyword,
            city=request.city,
            state=request.state,
            max_results=request.max_results
        )

        # Store results
        db.set_current_results(results)

        # Add to history
        db.add_history({
            "keyword": request.keyword,
            "city": request.city,
            "state": request.state,
            "max_results": request.max_results,
            "result_count": len(results)
        })

        return {
            "status": "success",
            "message": f"Found {len(results)} results",
            "count": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


# Results Endpoint
@app.get("/results")
async def get_results():
    """Get current search results."""
    results = db.get_current_results()
    return {
        "status": "success",
        "count": len(results),
        "results": results
    }


# History Endpoints
@app.get("/history")
async def get_history():
    """Get search history."""
    history = db.get_history()
    return {
        "status": "success",
        "count": len(history),
        "history": history
    }


@app.post("/history")
async def add_history(request: HistoryRequest):
    """Add a search to history."""
    try:
        entry = db.add_history(request.params)
        return {
            "status": "success",
            "message": "History entry added",
            "entry": entry
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add history: {str(e)}")


# Leads (Bookmarks) Endpoints
@app.get("/leads")
async def get_leads():
    """Get all saved/bookmarked leads."""
    leads = db.get_leads()
    return {
        "status": "success",
        "count": len(leads),
        "leads": leads
    }


@app.post("/leads")
async def save_lead(request: LeadRequest):
    """Save a lead to bookmarks."""
    try:
        lead_data = request.model_dump()
        lead = db.add_lead(lead_data)
        return {
            "status": "success",
            "message": "Lead saved successfully",
            "lead": lead
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save lead: {str(e)}")


@app.delete("/leads/{lead_id}")
async def delete_lead(lead_id: str):
    """Remove a lead from bookmarks."""
    try:
        success = db.delete_lead(lead_id)
        if success:
            return {
                "status": "success",
                "message": "Lead deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Lead not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete lead: {str(e)}")


# CSV Download Endpoint
@app.get("/download-csv")
async def download_csv():
    """Download current results as CSV file."""
    try:
        results = db.get_current_results()

        if not results:
            raise HTTPException(status_code=404, detail="No results to download")

        # Create CSV in memory
        output = io.StringIO()
        fieldnames = [
            "id", "name", "role", "company", "platform", "contact_link",
            "region", "notes", "rating", "review_count", "address",
            "phone", "website", "place_id"
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow({k: result.get(k, "") for k in fieldnames})

        # Convert to bytes for streaming
        output.seek(0)
        csv_bytes = io.BytesIO(output.getvalue().encode('utf-8'))

        return StreamingResponse(
            csv_bytes,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=leads.csv"}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate CSV: {str(e)}")


# Cost Analysis Endpoint
@app.get("/api/cost-analysis")
async def get_cost_analysis():
    """
    Parse and return the cost estimation markdown as structured JSON.
    Reads docs/COST_ESTIMATION.md and converts it to a renderable format.
    """
    try:
        docs_path = Path(__file__).parent.parent / "docs" / "COST_ESTIMATION.md"

        if not docs_path.exists():
            raise HTTPException(status_code=404, detail="Cost estimation document not found")

        with open(docs_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse markdown into structured sections
        sections = []
        current_section = None
        current_subsection = None
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]

            # H1 headers (# Title)
            if line.startswith('# ') and not line.startswith('## '):
                current_section = {
                    'type': 'title',
                    'level': 1,
                    'content': line.replace('# ', '').strip(),
                    'subsections': []
                }
                sections.append(current_section)

            # H2 headers (## Section)
            elif line.startswith('## '):
                current_subsection = {
                    'type': 'section',
                    'level': 2,
                    'title': line.replace('## ', '').strip(),
                    'content': []
                }
                if current_section:
                    current_section['subsections'].append(current_subsection)
                else:
                    sections.append(current_subsection)

            # H3 headers (### Subsection)
            elif line.startswith('### '):
                sub = {
                    'type': 'subsection',
                    'level': 3,
                    'title': line.replace('### ', '').strip(),
                    'content': []
                }
                if current_subsection:
                    current_subsection['content'].append(sub)
                    # Update pointer for nested content
                    current_content_target = sub['content']
                else:
                    sections.append(sub)

            # Tables (starts with |)
            elif line.strip().startswith('|') and '|' in line:
                # Parse table
                table_lines = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    table_lines.append(lines[i])
                    i += 1
                i -= 1  # Back up one since we'll increment at loop end

                if len(table_lines) >= 2:
                    # Parse header
                    headers = [cell.strip() for cell in table_lines[0].split('|')[1:-1]]
                    # Skip separator line (table_lines[1])
                    # Parse rows
                    rows = []
                    for row_line in table_lines[2:]:
                        cells = [cell.strip() for cell in row_line.split('|')[1:-1]]
                        if cells:
                            rows.append(cells)

                    table = {
                        'type': 'table',
                        'headers': headers,
                        'rows': rows
                    }

                    if current_subsection:
                        current_subsection['content'].append(table)
                    else:
                        sections.append(table)

            # Bullet points
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                bullet_items = []
                while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                    bullet_items.append(lines[i].strip()[2:])
                    i += 1
                i -= 1

                if current_subsection:
                    current_subsection['content'].append({
                        'type': 'list',
                        'items': bullet_items
                    })
                else:
                    sections.append({
                        'type': 'list',
                        'items': bullet_items
                    })

            # Bold text (**text**)
            elif '**' in line:
                if current_subsection:
                    current_subsection['content'].append({
                        'type': 'paragraph',
                        'content': line.strip()
                    })

            # Regular paragraph
            elif line.strip() and not line.startswith('#') and not line.startswith('---'):
                if current_subsection:
                    current_subsection['content'].append({
                        'type': 'paragraph',
                        'content': line.strip()
                    })

            i += 1

        return {
            "status": "success",
            "data": {
                "title": "Cost Estimation - Outreach Scraping Toolkit",
                "sections": sections
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse cost analysis: {str(e)}")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    db.initialize()
    print("✅ Database initialized")
