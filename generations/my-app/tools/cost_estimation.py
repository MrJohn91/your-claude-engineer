"""
Cost Estimation Tool for Apify Scraping
Calculate estimated costs based on number of profiles and actors used
"""

# Apify pricing (as of template creation - verify current prices)
APIFY_PRICING = {
    "compute_units_per_dollar": 10,  # $1 = 10 compute units
    "linkedin_actor_cu_per_profile": 0.05,  # Estimated CU per LinkedIn profile
    "instagram_actor_cu_per_profile": 0.03,  # Estimated CU per Instagram profile
}

def estimate_linkedin_cost(num_profiles: int) -> dict:
    """
    Estimate cost for scraping LinkedIn profiles

    Args:
        num_profiles: Number of LinkedIn profiles to scrape

    Returns:
        Dictionary with cost breakdown
    """
    compute_units = num_profiles * APIFY_PRICING["linkedin_actor_cu_per_profile"]
    estimated_cost = compute_units / APIFY_PRICING["compute_units_per_dollar"]

    return {
        "num_profiles": num_profiles,
        "compute_units": compute_units,
        "estimated_cost_usd": round(estimated_cost, 2),
        "platform": "LinkedIn"
    }

def estimate_instagram_cost(num_profiles: int) -> dict:
    """
    Estimate cost for scraping Instagram profiles

    Args:
        num_profiles: Number of Instagram profiles to scrape

    Returns:
        Dictionary with cost breakdown
    """
    compute_units = num_profiles * APIFY_PRICING["instagram_actor_cu_per_profile"]
    estimated_cost = compute_units / APIFY_PRICING["compute_units_per_dollar"]

    return {
        "num_profiles": num_profiles,
        "compute_units": compute_units,
        "estimated_cost_usd": round(estimated_cost, 2),
        "platform": "Instagram"
    }

def estimate_total_cost(linkedin_profiles: int, instagram_profiles: int) -> dict:
    """
    Estimate total cost for both platforms

    Args:
        linkedin_profiles: Number of LinkedIn profiles
        instagram_profiles: Number of Instagram profiles

    Returns:
        Dictionary with total cost breakdown
    """
    linkedin_cost = estimate_linkedin_cost(linkedin_profiles)
    instagram_cost = estimate_instagram_cost(instagram_profiles)

    total_cost = linkedin_cost["estimated_cost_usd"] + instagram_cost["estimated_cost_usd"]
    total_cu = linkedin_cost["compute_units"] + instagram_cost["compute_units"]

    return {
        "linkedin": linkedin_cost,
        "instagram": instagram_cost,
        "total_compute_units": round(total_cu, 2),
        "total_cost_usd": round(total_cost, 2)
    }

if __name__ == "__main__":
    # Example usage
    print("Cost Estimation Examples:")
    print("\nLinkedIn (100 profiles):")
    print(estimate_linkedin_cost(100))

    print("\nInstagram (100 profiles):")
    print(estimate_instagram_cost(100))

    print("\nTotal (100 LinkedIn + 100 Instagram):")
    print(estimate_total_cost(100, 100))
