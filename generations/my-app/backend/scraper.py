"""
Apify Integration Module
Handles LinkedIn and Instagram scraping via Apify actors
"""
import os
import random
from typing import List, Optional
from datetime import datetime
from .models import ContactSchema, Platform, ScrapeRequest


class ApifyScraperService:
    """
    Service class for Apify scraping operations
    For demo purposes, this generates realistic mock data.
    In production, this would integrate with Apify API.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("APIFY_API_KEY", "mock_key")
        self.scraped_data: List[ContactSchema] = []

        # Sample data pools for realistic generation
        self.first_names = [
            "Sarah", "Michael", "Jennifer", "David", "Jessica", "James",
            "Emily", "Robert", "Ashley", "William", "Amanda", "John",
            "Sophia", "Daniel", "Olivia", "Matthew", "Emma", "Christopher"
        ]
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
            "Miller", "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson",
            "Taylor", "Thomas", "Moore", "Jackson", "Martin", "Lee"
        ]
        self.roles = {
            "Technology": [
                "Senior Software Engineer", "Product Manager", "CTO",
                "Data Scientist", "DevOps Engineer", "Engineering Manager",
                "Full Stack Developer", "UI/UX Designer", "Solutions Architect"
            ],
            "Finance": [
                "Financial Analyst", "Investment Manager", "CFO",
                "Risk Manager", "Portfolio Manager", "Financial Advisor",
                "Quantitative Analyst", "Compliance Officer"
            ],
            "Marketing": [
                "Marketing Director", "Content Strategist", "SEO Specialist",
                "Brand Manager", "Social Media Manager", "Growth Hacker",
                "Marketing Analyst", "CMO"
            ],
            "Healthcare": [
                "Healthcare Administrator", "Clinical Director", "Medical Director",
                "Practice Manager", "Healthcare Consultant", "Nurse Manager"
            ],
            "Education": [
                "Education Director", "Curriculum Developer", "Dean",
                "Academic Advisor", "Training Manager", "Learning Specialist"
            ]
        }
        self.companies = {
            "Technology": [
                "TechCorp", "InnovateLabs", "CloudSoft", "DataDynamics",
                "AI Ventures", "CodeCrafters", "Quantum Systems", "ByteWorks"
            ],
            "Finance": [
                "Capital Partners", "Investment Group", "Financial Services Inc",
                "Wealth Management Co", "Asset Holdings", "Equity Advisors"
            ],
            "Marketing": [
                "Marketing Pros", "Brand Builders", "Digital Strategies",
                "Growth Agency", "Creative Studio", "Media Innovations"
            ],
            "Healthcare": [
                "HealthCare Plus", "Medical Group", "Wellness Center",
                "Care Providers", "Health Solutions", "Medical Partners"
            ],
            "Education": [
                "Learning Academy", "Education Partners", "Training Institute",
                "Academic Solutions", "Knowledge Hub", "EdTech Innovations"
            ]
        }
        self.regions = [
            "San Francisco, CA", "New York, NY", "Austin, TX", "Boston, MA",
            "Seattle, WA", "Los Angeles, CA", "Chicago, IL", "Denver, CO",
            "Portland, OR", "Atlanta, GA", "Miami, FL", "Washington, DC"
        ]

    async def scrape(self, request: ScrapeRequest) -> List[ContactSchema]:
        """
        Main scraping method that generates mock data based on filters
        In production, this would call Apify actors for each platform
        """
        results = []
        results_per_platform = request.max_results // len(request.platforms) if request.platforms else request.max_results

        for platform in request.platforms:
            platform_results = await self._scrape_platform(
                platform=platform,
                industries=request.industries or ["Technology", "Finance", "Marketing"],
                roles=request.roles or [],
                regions=request.regions or self.regions,
                max_results=results_per_platform
            )
            results.extend(platform_results)

        # Store for later retrieval
        self.scraped_data = results
        return results

    async def _scrape_platform(
        self,
        platform: Platform,
        industries: List[str],
        roles: List[str],
        regions: List[str],
        max_results: int
    ) -> List[ContactSchema]:
        """
        Scrape a specific platform (mock implementation)
        """
        results = []

        for i in range(max_results):
            # Randomly select from filters
            industry = random.choice(industries) if industries else "Technology"
            region = random.choice(regions) if regions else random.choice(self.regions)

            # Get role based on industry or from filter
            if roles:
                role = random.choice(roles)
            else:
                industry_roles = self.roles.get(industry, self.roles["Technology"])
                role = random.choice(industry_roles)

            # Generate contact
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            full_name = f"{first_name} {last_name}"

            # Get company based on industry
            industry_companies = self.companies.get(industry, self.companies["Technology"])
            company = random.choice(industry_companies)

            # Generate platform-specific URL
            username = f"{first_name.lower()}{last_name.lower()}"
            if platform == Platform.LINKEDIN:
                contact_link = f"https://linkedin.com/in/{username}"
            elif platform == Platform.INSTAGRAM:
                contact_link = f"https://instagram.com/{username}"
            elif platform == Platform.TWITTER:
                contact_link = f"https://twitter.com/{username}"
            else:
                contact_link = f"https://facebook.com/{username}"

            # Generate notes
            notes_templates = [
                f"Experienced in {industry.lower()} with 5+ years",
                f"Active on {platform.value}, posts about {industry.lower()}",
                f"Based in {region}, open to collaborations",
                f"Passionate about innovation in {industry.lower()}",
                f"Seeking partnerships and networking opportunities"
            ]
            notes = random.choice(notes_templates)

            contact = ContactSchema(
                name=full_name,
                role=role,
                company=company,
                platform=platform,
                contact_link=contact_link,
                region=region,
                notes=notes
            )
            results.append(contact)

        return results

    async def get_results(self, limit: int = 50, offset: int = 0) -> List[ContactSchema]:
        """
        Get scraped results with pagination
        """
        return self.scraped_data[offset:offset + limit]

    def get_total_results(self) -> int:
        """
        Get total number of scraped results
        """
        return len(self.scraped_data)

    async def scrape_linkedin_profiles(self, search_query: str, max_results: int = 100):
        """
        Scrape LinkedIn profiles based on search query
        Legacy method - kept for compatibility
        """
        request = ScrapeRequest(
            platforms=[Platform.LINKEDIN],
            search_query=search_query,
            max_results=max_results
        )
        return await self.scrape(request)

    async def scrape_instagram_profiles(self, hashtags: list[str], max_results: int = 100):
        """
        Scrape Instagram profiles based on hashtags
        Legacy method - kept for compatibility
        """
        request = ScrapeRequest(
            platforms=[Platform.INSTAGRAM],
            search_query=" ".join(hashtags),
            max_results=max_results
        )
        return await self.scrape(request)

    async def get_scraping_status(self, run_id: str):
        """
        Check the status of a scraping job
        In production, this would check Apify run status
        """
        return {
            "run_id": run_id,
            "status": "completed",
            "progress": 100,
            "total_results": len(self.scraped_data)
        }
