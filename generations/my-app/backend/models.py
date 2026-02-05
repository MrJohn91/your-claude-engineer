"""
Data models for the Outreach Scraping Toolkit
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum


class Platform(str, Enum):
    """Supported platforms for scraping"""
    LINKEDIN = "LinkedIn"
    INSTAGRAM = "Instagram"
    TWITTER = "Twitter"
    FACEBOOK = "Facebook"


class ContactSchema(BaseModel):
    """Output schema for scraped contact data"""
    name: str = Field(..., description="Full name of the contact")
    role: str = Field(..., description="Job title or role")
    company: str = Field(..., description="Company name")
    platform: Platform = Field(..., description="Platform where contact was found")
    contact_link: str = Field(..., description="Profile URL or contact link")
    region: str = Field(..., description="Geographic region")
    notes: Optional[str] = Field(None, description="Additional notes or bio")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "role": "Senior Software Engineer",
                "company": "Tech Corp",
                "platform": "LinkedIn",
                "contact_link": "https://linkedin.com/in/johndoe",
                "region": "San Francisco, CA",
                "notes": "Specializes in cloud infrastructure"
            }
        }


class ScrapeRequest(BaseModel):
    """Request model for scraping operation"""
    platforms: List[Platform] = Field(..., min_length=1, description="Platforms to scrape")
    industries: Optional[List[str]] = Field(default=[], description="Target industries")
    roles: Optional[List[str]] = Field(default=[], description="Target job roles")
    regions: Optional[List[str]] = Field(default=[], description="Target geographic regions")
    search_query: Optional[str] = Field(default="", description="Additional search query")
    max_results: int = Field(default=50, ge=1, le=500, description="Maximum results per platform")

    class Config:
        json_schema_extra = {
            "example": {
                "platforms": ["LinkedIn", "Instagram"],
                "industries": ["Technology", "Finance"],
                "roles": ["Software Engineer", "Product Manager"],
                "regions": ["San Francisco", "New York"],
                "search_query": "startup founder",
                "max_results": 100
            }
        }


class ScrapeResponse(BaseModel):
    """Response model for scraping operation"""
    status: str = Field(..., description="Status of the scrape operation")
    message: str = Field(..., description="Human-readable message")
    job_id: Optional[str] = Field(None, description="Job ID for tracking")
    total_results: int = Field(default=0, description="Total results scraped")


class ResultsResponse(BaseModel):
    """Response model for results retrieval"""
    total: int = Field(..., description="Total number of results")
    limit: int = Field(..., description="Results per page")
    offset: int = Field(..., description="Current offset")
    data: List[ContactSchema] = Field(..., description="List of contacts")


class ExportSheetRequest(BaseModel):
    """Request model for Google Sheets export"""
    sheet_title: Optional[str] = Field(None, description="Title for the new sheet")
    sheet_id: Optional[str] = Field(None, description="Existing sheet ID to append to")
    include_notes: bool = Field(default=True, description="Include notes column")

    class Config:
        json_schema_extra = {
            "example": {
                "sheet_title": "Outreach Leads - Q1 2024",
                "include_notes": True
            }
        }


class ExportSheetResponse(BaseModel):
    """Response model for Google Sheets export"""
    status: str = Field(..., description="Status of export operation")
    message: str = Field(..., description="Human-readable message")
    sheet_url: Optional[str] = Field(None, description="URL to the Google Sheet")
    sheet_id: Optional[str] = Field(None, description="Google Sheet ID")
