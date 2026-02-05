"""
Google Sheets Export Module
Handles exporting scraped data to Google Sheets
"""
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import ContactSchema


class GoogleSheetsService:
    """
    Service class for Google Sheets operations
    For demo purposes, this provides mock Google Sheets functionality.
    In production, this would integrate with gspread and Google Sheets API.
    """

    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_SHEETS_CREDENTIALS_PATH",
            "./config/google-credentials.json"
        )
        self.enabled = os.getenv("GOOGLE_SHEETS_ENABLED", "false").lower() == "true"

        # Mock storage for demo
        self.mock_sheets: Dict[str, List[Dict]] = {}

    async def export_to_sheet(
        self,
        data: List[ContactSchema],
        sheet_id: Optional[str] = None,
        sheet_title: Optional[str] = None,
        include_notes: bool = True
    ) -> Dict[str, Any]:
        """
        Export scraped data to Google Sheets
        If sheet_id is None, create a new sheet
        """
        if not data:
            return {
                "status": "error",
                "message": "No data to export",
                "sheet_url": None,
                "sheet_id": None
            }

        # In production, this would use gspread to write to Google Sheets
        # For demo, we'll simulate the export

        if sheet_id:
            # Append to existing sheet
            result = await self.append_to_sheet(data, sheet_id)
        else:
            # Create new sheet
            title = sheet_title or f"Outreach Leads - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            result = await self.create_new_sheet(title, data)

        return result

    async def create_new_sheet(
        self,
        title: str,
        data: Optional[List[ContactSchema]] = None
    ) -> Dict[str, Any]:
        """
        Create a new Google Sheet
        In production, this would use gspread.create()
        """
        # Generate mock sheet ID
        sheet_id = f"mock_sheet_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Convert data to rows
        rows = []
        if data:
            # Header row
            header = ["Name", "Role", "Company", "Platform", "Contact Link", "Region", "Notes"]
            rows.append(header)

            # Data rows
            for contact in data:
                row = [
                    contact.name,
                    contact.role,
                    contact.company,
                    contact.platform.value,
                    contact.contact_link,
                    contact.region,
                    contact.notes or ""
                ]
                rows.append(row)

        # Store in mock storage
        self.mock_sheets[sheet_id] = {
            "title": title,
            "data": rows,
            "created_at": datetime.now().isoformat(),
            "row_count": len(rows)
        }

        # Generate mock URL
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

        return {
            "status": "success",
            "message": f"Successfully created sheet '{title}' with {len(data) if data else 0} contacts",
            "sheet_url": sheet_url,
            "sheet_id": sheet_id
        }

    async def append_to_sheet(
        self,
        data: List[ContactSchema],
        sheet_id: str
    ) -> Dict[str, Any]:
        """
        Append data to existing Google Sheet
        In production, this would use gspread.append_rows()
        """
        if sheet_id not in self.mock_sheets:
            return {
                "status": "error",
                "message": f"Sheet with ID {sheet_id} not found",
                "sheet_url": None,
                "sheet_id": sheet_id
            }

        # Get existing sheet
        sheet = self.mock_sheets[sheet_id]

        # Append new rows
        for contact in data:
            row = [
                contact.name,
                contact.role,
                contact.company,
                contact.platform.value,
                contact.contact_link,
                contact.region,
                contact.notes or ""
            ]
            sheet["data"].append(row)

        sheet["row_count"] = len(sheet["data"])
        sheet["updated_at"] = datetime.now().isoformat()

        # Generate URL
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

        return {
            "status": "success",
            "message": f"Successfully appended {len(data)} contacts to sheet",
            "sheet_url": sheet_url,
            "sheet_id": sheet_id
        }

    async def get_sheet_info(self, sheet_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a sheet
        """
        return self.mock_sheets.get(sheet_id)

    def _format_data_for_export(
        self,
        data: List[ContactSchema],
        include_notes: bool = True
    ) -> List[List[str]]:
        """
        Format contact data for Google Sheets export
        """
        # Header row
        headers = ["Name", "Role", "Company", "Platform", "Contact Link", "Region"]
        if include_notes:
            headers.append("Notes")

        rows = [headers]

        # Data rows
        for contact in data:
            row = [
                contact.name,
                contact.role,
                contact.company,
                contact.platform.value,
                contact.contact_link,
                contact.region
            ]
            if include_notes:
                row.append(contact.notes or "")

            rows.append(row)

        return rows

    def check_credentials(self) -> bool:
        """
        Check if Google Sheets credentials are configured
        """
        if not self.enabled:
            return False

        # In production, check if credentials file exists
        try:
            return os.path.exists(self.credentials_path)
        except Exception:
            return False
