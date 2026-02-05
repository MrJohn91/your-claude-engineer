"""
FastAPI Backend for Outreach Scraping Toolkit
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yaml
from pathlib import Path
from typing import Dict, List

app = FastAPI(title="Outreach Scraping Toolkit")

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

@app.on_event("startup")
async def load_audience_config():
    """Load audience configuration from YAML file"""
    global AUDIENCE_CONFIG
    config_path = Path(__file__).parent.parent / "config" / "audience.yaml"

    try:
        with open(config_path, 'r') as f:
            AUDIENCE_CONFIG = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: Audience config file not found at {config_path}")
        AUDIENCE_CONFIG = {
            "platforms": [],
            "industries": [],
            "roles": [],
            "regions": []
        }
    except Exception as e:
        print(f"Error loading audience config: {e}")
        AUDIENCE_CONFIG = {
            "platforms": [],
            "industries": [],
            "roles": [],
            "regions": []
        }

@app.get("/")
async def root():
    return {"message": "Outreach Scraping Toolkit API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/config/audience")
async def get_audience_config():
    """Get target audience configuration for filter options"""
    if not AUDIENCE_CONFIG:
        raise HTTPException(status_code=500, detail="Audience configuration not loaded")
    return AUDIENCE_CONFIG

# TODO: Add scraping endpoints
# TODO: Add Google Sheets export endpoints
# TODO: Add cost estimation endpoints
