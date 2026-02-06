"""
Apify integration module for Google Maps scraping.
Falls back to mock data if APIFY_API_TOKEN is not configured.
"""
import os
import uuid
from typing import List, Dict
from apify_client import ApifyClient


def generate_mock_data(keyword: str, city: str, state: str, max_results: int = 10) -> List[Dict]:
    """Generate realistic mock data for development."""
    mock_businesses = [
        {"name": "TechHub Berlin", "type": "Coworking Space", "rating": 4.7, "reviews": 342},
        {"name": "StartupCafe", "type": "Coffee Shop", "rating": 4.5, "reviews": 189},
        {"name": "Innovation Labs GmbH", "type": "Business Center", "rating": 4.8, "reviews": 276},
        {"name": "Digital Minds", "type": "Consulting Agency", "rating": 4.6, "reviews": 154},
        {"name": "Code & Coffee", "type": "Cafe", "rating": 4.4, "reviews": 423},
        {"name": "FutureTech Solutions", "type": "Software Company", "rating": 4.9, "reviews": 98},
        {"name": "Green Valley Restaurant", "type": "Restaurant", "rating": 4.3, "reviews": 567},
        {"name": "Metro Business Park", "type": "Office Complex", "rating": 4.5, "reviews": 234},
        {"name": "Creative Studio", "type": "Design Agency", "rating": 4.7, "reviews": 187},
        {"name": "Global Trade Center", "type": "Business Center", "rating": 4.6, "reviews": 312},
        {"name": "Artisan Bakery", "type": "Bakery", "rating": 4.8, "reviews": 645},
        {"name": "Urban Fitness Club", "type": "Gym", "rating": 4.4, "reviews": 289},
        {"name": "Smart Solutions Inc", "type": "Consulting Firm", "rating": 4.7, "reviews": 156},
        {"name": "Moonlight Bar & Grill", "type": "Restaurant", "rating": 4.5, "reviews": 478},
        {"name": "NextGen Academy", "type": "Training Center", "rating": 4.9, "reviews": 234},
    ]

    results = []
    for i in range(min(max_results, len(mock_businesses))):
        biz = mock_businesses[i]
        place_id = f"ChIJ{uuid.uuid4().hex[:16]}"

        results.append({
            "id": f"mock_{uuid.uuid4().hex[:8]}",
            "name": biz["name"],
            "role": "",
            "company": biz["name"],
            "platform": "Google Maps",
            "contact_link": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
            "region": f"{city}, {state}",
            "notes": f"{keyword} - {biz['type']}",
            "rating": biz["rating"],
            "review_count": biz["reviews"],
            "address": f"{i+1} {city} Street, {city}, {state}",
            "phone": f"+49-{30+i}-{1000+i*111}-{i*10}",
            "website": f"https://www.{biz['name'].lower().replace(' ', '')}.com",
            "place_id": place_id
        })

    return results


def scrape_google_maps(keyword: str, city: str, state: str, max_results: int = 20) -> List[Dict]:
    """
    Scrape Google Maps using Apify API.
    Falls back to mock data if APIFY_API_TOKEN is not set.

    Args:
        keyword: Audience-focused search (e.g., "AI founders", "Web3 startups", "tech BD leads")
        city: City or area (e.g., Berlin, Singapore)
        state: Region or country (e.g., Germany, South Asia)
        max_results: Maximum number of results to return

    Returns:
        List of business records matching the output schema
    """
    apify_token = os.getenv("APIFY_API_TOKEN")

    # Return mock data if no API token
    if not apify_token or apify_token == "your_apify_api_token_here":
        print("⚠️  No Apify API token found - returning mock data")
        return generate_mock_data(keyword, city, state, max_results)

    try:
        # Initialize Apify client
        client = ApifyClient(apify_token)

        # Prepare the Actor input
        search_query = f"{keyword} in {city}, {state}"
        run_input = {
            "searchStringsArray": [search_query],
            "maxCrawledPlacesPerSearch": max_results,
            "language": "en",
            "includeWebResults": True,
            "scrapeReviews": False,
        }

        # Run the Actor and wait for it to finish
        print(f"🚀 Starting Apify scrape: {search_query}")
        run = client.actor("compass/crawler-google-places").call(run_input=run_input)

        # Fetch results from the Actor's dataset
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            place_id = item.get("placeId", "")

            result = {
                "id": f"apify_{uuid.uuid4().hex[:8]}",
                "name": item.get("title", "Unknown"),
                "role": "",
                "company": item.get("title", "Unknown"),
                "platform": "Google Maps",
                "contact_link": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                "region": f"{city}, {state}",
                "notes": f"{keyword}",
                "rating": item.get("totalScore", 0),
                "review_count": item.get("reviewsCount", 0),
                "address": item.get("address", ""),
                "phone": item.get("phone", ""),
                "website": item.get("website", ""),
                "place_id": place_id
            }
            results.append(result)

        print(f"✅ Apify scrape completed: {len(results)} results")
        return results

    except Exception as e:
        print(f"❌ Apify scrape failed: {str(e)}")
        print("⚠️  Falling back to mock data")
        return generate_mock_data(keyword, city, state, max_results)
