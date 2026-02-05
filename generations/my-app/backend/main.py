"""
FastAPI Backend for Outreach Scraping Toolkit
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Outreach Scraping Toolkit")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Outreach Scraping Toolkit API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# TODO: Add scraping endpoints
# TODO: Add Google Sheets export endpoints
# TODO: Add cost estimation endpoints
