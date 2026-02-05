"""
FastAPI Backend for Outreach Scraping Toolkit
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import yaml
import csv
import io
import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import uuid

from models import (
    ContactSchema,
    ScrapeRequest,
    ScrapeResponse,
    ResultsResponse,
    ExportSheetRequest,
    ExportSheetResponse
)
from scraper import ApifyScraperService
from sheets import GoogleSheetsService

app = FastAPI(
    title="Outreach Scraping Toolkit",
    description="API for multi-platform contact scraping and outreach management",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load audience configuration at startup
AUDIENCE_CONFIG: Dict[str, List[str]] = {}

# Initialize services
scraper_service: ApifyScraperService = None
sheets_service: GoogleSheetsService = None


@app.on_event("startup")
async def startup_event():
    """Initialize services and load configuration on startup"""
    global AUDIENCE_CONFIG, scraper_service, sheets_service

    # Load audience configuration
    config_path = Path(__file__).parent.parent / "config" / "audience.yaml"

    try:
        with open(config_path, 'r') as f:
            AUDIENCE_CONFIG = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: Audience config file not found at {config_path}")
        AUDIENCE_CONFIG = {
            "platforms": ["LinkedIn", "Instagram", "Twitter", "Facebook"],
            "industries": ["Technology", "Finance", "Marketing", "Healthcare", "Education"],
            "roles": ["Engineer", "Manager", "Director", "Executive"],
            "regions": ["San Francisco, CA", "New York, NY", "Austin, TX"]
        }
    except Exception as e:
        print(f"Error loading audience config: {e}")
        AUDIENCE_CONFIG = {
            "platforms": ["LinkedIn", "Instagram", "Twitter", "Facebook"],
            "industries": ["Technology", "Finance", "Marketing", "Healthcare", "Education"],
            "roles": ["Engineer", "Manager", "Director", "Executive"],
            "regions": ["San Francisco, CA", "New York, NY", "Austin, TX"]
        }

    # Initialize services
    apify_key = os.getenv("APIFY_API_KEY")
    scraper_service = ApifyScraperService(api_key=apify_key)

    google_creds = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
    sheets_service = GoogleSheetsService(credentials_path=google_creds)

    print("✅ Services initialized successfully")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
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


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "scraper": scraper_service is not None,
            "sheets": sheets_service is not None
        }
    }


@app.get("/api/config/audience")
async def get_audience_config():
    """Get target audience configuration for filter options"""
    if not AUDIENCE_CONFIG:
        raise HTTPException(status_code=500, detail="Audience configuration not loaded")
    return AUDIENCE_CONFIG


@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_contacts(request: ScrapeRequest):
    """
    Start a scraping job with specified filters

    This endpoint accepts filter parameters and initiates a scraping operation
    across the selected platforms. Returns a job ID for tracking.
    """
    if not scraper_service:
        raise HTTPException(
            status_code=503,
            detail="Scraper service not initialized"
        )

    try:
        # Validate platforms
        if not request.platforms:
            raise HTTPException(
                status_code=400,
                detail="At least one platform must be specified"
            )

        # Execute scraping
        results = await scraper_service.scrape(request)

        # Generate job ID
        job_id = str(uuid.uuid4())

        return ScrapeResponse(
            status="success",
            message=f"Successfully scraped {len(results)} contacts from {len(request.platforms)} platform(s)",
            job_id=job_id,
            total_results=len(results)
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scraping failed: {str(e)}"
        )


@app.get("/api/results", response_model=ResultsResponse)
async def get_results(
    limit: int = Query(default=50, ge=1, le=500, description="Number of results per page"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination")
):
    """
    Retrieve scraped results with pagination

    Returns the scraped contact data in the defined schema with pagination support.
    """
    if not scraper_service:
        raise HTTPException(
            status_code=503,
            detail="Scraper service not initialized"
        )

    try:
        # Get results with pagination
        results = await scraper_service.get_results(limit=limit, offset=offset)
        total = scraper_service.get_total_results()

        return ResultsResponse(
            total=total,
            limit=limit,
            offset=offset,
            data=results
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve results: {str(e)}"
        )


@app.post("/api/export-sheet", response_model=ExportSheetResponse)
async def export_to_sheet(request: ExportSheetRequest):
    """
    Export scraped results to Google Sheets

    Creates a new Google Sheet or appends to an existing one with the scraped data.
    Returns the sheet URL and ID.
    """
    if not sheets_service:
        raise HTTPException(
            status_code=503,
            detail="Google Sheets service not initialized"
        )

    if not scraper_service:
        raise HTTPException(
            status_code=503,
            detail="Scraper service not initialized"
        )

    try:
        # Get all results (no pagination for export)
        all_results = await scraper_service.get_results(limit=10000, offset=0)

        if not all_results:
            raise HTTPException(
                status_code=400,
                detail="No data available to export. Please run a scrape first."
            )

        # Export to Google Sheets
        result = await sheets_service.export_to_sheet(
            data=all_results,
            sheet_id=request.sheet_id,
            sheet_title=request.sheet_title,
            include_notes=request.include_notes
        )

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        return ExportSheetResponse(
            status=result["status"],
            message=result["message"],
            sheet_url=result["sheet_url"],
            sheet_id=result["sheet_id"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Export to Google Sheets failed: {str(e)}"
        )


@app.get("/api/download-csv")
async def download_csv(
    filename: str = Query(default=None, description="Custom filename for the CSV")
):
    """
    Download scraped results as CSV file

    Returns a downloadable CSV file with all scraped contact data.
    """
    if not scraper_service:
        raise HTTPException(
            status_code=503,
            detail="Scraper service not initialized"
        )

    try:
        # Get all results (no pagination for download)
        all_results = await scraper_service.get_results(limit=10000, offset=0)

        if not all_results:
            raise HTTPException(
                status_code=400,
                detail="No data available to download. Please run a scrape first."
            )

        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        headers = ["Name", "Role", "Company", "Platform", "Contact Link", "Region", "Notes"]
        writer.writerow(headers)

        # Write data rows
        for contact in all_results:
            row = [
                contact.name,
                contact.role,
                contact.company,
                contact.platform.value,
                contact.contact_link,
                contact.region,
                contact.notes or ""
            ]
            writer.writerow(row)

        # Prepare response
        output.seek(0)
        csv_filename = filename or f"outreach_contacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={csv_filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"CSV download failed: {str(e)}"
        )


@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    """
    Check the status of a scraping job

    Returns the current status and progress of a scraping operation.
    """
    if not scraper_service:
        raise HTTPException(
            status_code=503,
            detail="Scraper service not initialized"
        )

    try:
        status = await scraper_service.get_scraping_status(job_id)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get job status: {str(e)}"
        )
