"""
Cost Estimation Tool for Outreach Scraping Toolkit

This script calculates cost estimates for various volume levels including:
- Apify/Scraping tool costs
- Proxy costs (residential vs datacenter)
- API usage costs (LinkedIn, X, etc.)
- AI enrichment/parsing costs

Outputs:
- CSV file with detailed cost breakdown
- Markdown table with formatted results
- Console output with nicely formatted tables

Usage:
    python cost_estimation.py
    python cost_estimation.py --volumes 1000 5000 25000
    python cost_estimation.py --output-dir ./custom_output

Author: Outreach Scraping Toolkit
Date: 2026-02-05
"""

import argparse
import csv
import sys
from typing import List, Dict, Tuple
from pathlib import Path


# ============================================================================
# PRICING CONSTANTS
# ============================================================================

# Apify/Scraping Costs (based on Apify marketplace data)
# Source: https://apify.com/pricing
SCRAPING_COSTS = {
    'cost_per_1k': (0.50, 1.00),      # Min-Max per 1k records
    'cost_per_10k': (4.50, 9.00),     # Min-Max per 10k records
    'cost_per_50k': (20.00, 40.00),   # Min-Max per 50k records
    'note': 'Costs vary by platform complexity and data richness'
}

# Proxy Costs (per GB and monthly estimates)
# Sources: BrightData, Oxylabs, SmartProxy pricing pages
PROXY_COSTS = {
    'residential_per_gb': (0.20, 0.50),    # Per GB
    'datacenter_per_gb': (0.05, 0.10),     # Per GB
    'typical_gb_per_1k': 0.5,              # Estimated GB per 1k records
    'monthly_baseline': (50, 300),         # Monthly cost for typical project
    'note': 'Residential proxies are 4-5x more expensive but have better success rates'
}

# API Costs (LinkedIn, X, etc.)
# Sources: Official API pricing pages (as of Jan 2025)
API_COSTS = {
    'linkedin_via_apify': 0,              # Included in Apify costs
    'x_api_basic': 100,                   # Per month (Basic tier)
    'x_api_pro': 500,                     # Per month (Pro tier)
    'x_api_enterprise': 2500,             # Per month (Enterprise tier)
    'other_platforms': 'varies',
    'note': 'LinkedIn scraping via Apify, X requires official API subscription'
}

# AI Enrichment Costs (optional add-on)
# Sources: Anthropic and OpenAI pricing pages
AI_ENRICHMENT_COSTS = {
    'claude_input_per_1k_tokens': 0.003,   # Claude 3.5 Sonnet
    'claude_output_per_1k_tokens': 0.015,  # Claude 3.5 Sonnet
    'gpt4_input_per_1k_tokens': 0.03,      # GPT-4 Turbo
    'gpt4_output_per_1k_tokens': 0.06,     # GPT-4 Turbo
    'avg_tokens_per_record': 500,          # Estimated tokens per enrichment
    'note': 'Claude is 10x cheaper than GPT-4 for similar quality'
}


# ============================================================================
# COST CALCULATION FUNCTIONS
# ============================================================================

def calculate_scraping_cost(volume: int) -> Tuple[float, float]:
    """
    Calculate scraping costs based on volume.

    Uses tiered pricing from SCRAPING_COSTS constants.

    Args:
        volume: Number of records to scrape

    Returns:
        Tuple of (min_cost, max_cost)
    """
    # Linear interpolation based on defined tiers
    if volume <= 1000:
        ratio = volume / 1000
        min_cost = SCRAPING_COSTS['cost_per_1k'][0] * ratio
        max_cost = SCRAPING_COSTS['cost_per_1k'][1] * ratio
    elif volume <= 10000:
        ratio = volume / 10000
        min_cost = SCRAPING_COSTS['cost_per_10k'][0] * ratio
        max_cost = SCRAPING_COSTS['cost_per_10k'][1] * ratio
    else:
        ratio = volume / 50000
        min_cost = SCRAPING_COSTS['cost_per_50k'][0] * ratio
        max_cost = SCRAPING_COSTS['cost_per_50k'][1] * ratio

    return round(min_cost, 2), round(max_cost, 2)


def calculate_proxy_cost(volume: int, proxy_type: str = 'residential') -> Tuple[float, float]:
    """
    Calculate proxy costs based on volume and type.

    Estimates GB usage based on typical data transfer per record.

    Args:
        volume: Number of records to scrape
        proxy_type: 'residential' or 'datacenter'

    Returns:
        Tuple of (min_cost, max_cost)
    """
    gb_needed = volume * PROXY_COSTS['typical_gb_per_1k'] / 1000

    if proxy_type == 'residential':
        cost_range = PROXY_COSTS['residential_per_gb']
    else:
        cost_range = PROXY_COSTS['datacenter_per_gb']

    min_cost = gb_needed * cost_range[0]
    max_cost = gb_needed * cost_range[1]

    return round(min_cost, 2), round(max_cost, 2)


def calculate_api_cost(volume: int, include_x_api: bool = True, x_tier: str = 'basic') -> float:
    """
    Calculate API costs.

    LinkedIn is included in Apify costs, but X API requires separate subscription.

    Args:
        volume: Number of records (for future scaling calculations)
        include_x_api: Whether to include X/Twitter API costs
        x_tier: X API tier ('basic', 'pro', 'enterprise')

    Returns:
        Monthly API cost
    """
    api_cost = 0

    if include_x_api:
        if x_tier == 'basic':
            api_cost = API_COSTS['x_api_basic']
        elif x_tier == 'pro':
            api_cost = API_COSTS['x_api_pro']
        else:
            api_cost = API_COSTS['x_api_enterprise']

    return api_cost


def calculate_ai_enrichment_cost(volume: int, ai_provider: str = 'claude') -> Tuple[float, float]:
    """
    Calculate AI enrichment costs.

    Assumes each record requires AI processing for data extraction/cleaning.

    Args:
        volume: Number of records to enrich
        ai_provider: 'claude' or 'gpt4'

    Returns:
        Tuple of (min_cost, max_cost) accounting for input/output tokens
    """
    total_tokens = volume * AI_ENRICHMENT_COSTS['avg_tokens_per_record']
    # Assume 60% input, 40% output split
    input_tokens = total_tokens * 0.6 / 1000
    output_tokens = total_tokens * 0.4 / 1000

    if ai_provider == 'claude':
        cost = (input_tokens * AI_ENRICHMENT_COSTS['claude_input_per_1k_tokens'] +
                output_tokens * AI_ENRICHMENT_COSTS['claude_output_per_1k_tokens'])
    else:  # gpt4
        cost = (input_tokens * AI_ENRICHMENT_COSTS['gpt4_input_per_1k_tokens'] +
                output_tokens * AI_ENRICHMENT_COSTS['gpt4_output_per_1k_tokens'])

    return round(cost, 2), round(cost, 2)


def calculate_total_cost(volume: int, include_ai: bool = False) -> Dict:
    """
    Calculate total cost breakdown for a given volume.

    Args:
        volume: Number of records
        include_ai: Whether to include AI enrichment costs

    Returns:
        Dictionary with detailed cost breakdown
    """
    scraping_min, scraping_max = calculate_scraping_cost(volume)
    proxy_res_min, proxy_res_max = calculate_proxy_cost(volume, 'residential')
    proxy_dc_min, proxy_dc_max = calculate_proxy_cost(volume, 'datacenter')
    api_cost = calculate_api_cost(volume, include_x_api=True, x_tier='basic')

    # Calculate totals with residential proxies (recommended)
    total_min_res = scraping_min + proxy_res_min + api_cost
    total_max_res = scraping_max + proxy_res_max + api_cost

    # Calculate totals with datacenter proxies (budget option)
    total_min_dc = scraping_min + proxy_dc_min + api_cost
    total_max_dc = scraping_max + proxy_dc_max + api_cost

    result = {
        'volume': volume,
        'scraping_cost': (scraping_min, scraping_max),
        'proxy_cost_residential': (proxy_res_min, proxy_res_max),
        'proxy_cost_datacenter': (proxy_dc_min, proxy_dc_max),
        'api_cost_monthly': api_cost,
        'total_residential': (total_min_res, total_max_res),
        'total_datacenter': (total_min_dc, total_max_dc),
        'cost_per_contact_residential': (round(total_min_res / volume, 4), round(total_max_res / volume, 4)),
        'cost_per_contact_datacenter': (round(total_min_dc / volume, 4), round(total_max_dc / volume, 4)),
    }

    if include_ai:
        ai_claude_min, ai_claude_max = calculate_ai_enrichment_cost(volume, 'claude')
        ai_gpt4_min, ai_gpt4_max = calculate_ai_enrichment_cost(volume, 'gpt4')
        result['ai_enrichment_claude'] = (ai_claude_min, ai_claude_max)
        result['ai_enrichment_gpt4'] = (ai_gpt4_min, ai_gpt4_max)

        # Add AI costs to totals
        result['total_residential_with_claude'] = (
            round(total_min_res + ai_claude_min, 2),
            round(total_max_res + ai_claude_max, 2)
        )
        result['total_residential_with_gpt4'] = (
            round(total_min_res + ai_gpt4_min, 2),
            round(total_max_res + ai_gpt4_max, 2)
        )

    return result


# ============================================================================
# OUTPUT FUNCTIONS
# ============================================================================

def format_cost_range(cost_tuple: Tuple[float, float]) -> str:
    """Format a cost range as a string."""
    return f"${cost_tuple[0]:.2f} - ${cost_tuple[1]:.2f}"


def print_console_output(results: List[Dict]):
    """Print formatted cost estimates to console."""
    print("\n" + "="*80)
    print("COST ESTIMATION REPORT - OUTREACH SCRAPING TOOLKIT")
    print("="*80)

    for result in results:
        volume = result['volume']
        print(f"\n{'─'*80}")
        print(f"VOLUME: {volume:,} records")
        print(f"{'─'*80}")

        print(f"\n  Scraping Costs:        {format_cost_range(result['scraping_cost'])}")
        print(f"  Proxy (Residential):   {format_cost_range(result['proxy_cost_residential'])}")
        print(f"  Proxy (Datacenter):    {format_cost_range(result['proxy_cost_datacenter'])}")
        print(f"  API Costs (Monthly):   ${result['api_cost_monthly']:.2f}")

        if 'ai_enrichment_claude' in result:
            print(f"  AI Enrichment (Claude): {format_cost_range(result['ai_enrichment_claude'])}")
            print(f"  AI Enrichment (GPT-4):  {format_cost_range(result['ai_enrichment_gpt4'])}")

        print(f"\n  TOTAL (Residential):   {format_cost_range(result['total_residential'])}")
        print(f"  TOTAL (Datacenter):    {format_cost_range(result['total_datacenter'])}")

        if 'total_residential_with_claude' in result:
            print(f"  TOTAL (+ Claude):      {format_cost_range(result['total_residential_with_claude'])}")
            print(f"  TOTAL (+ GPT-4):       {format_cost_range(result['total_residential_with_gpt4'])}")

        print(f"\n  Cost per Contact:")
        print(f"    Residential:         {format_cost_range(result['cost_per_contact_residential'])}")
        print(f"    Datacenter:          {format_cost_range(result['cost_per_contact_datacenter'])}")

    print("\n" + "="*80)
    print("ASSUMPTIONS & SOURCES")
    print("="*80)
    print(f"\nScraping: {SCRAPING_COSTS['note']}")
    print(f"  Source: Apify marketplace pricing (https://apify.com/pricing)")
    print(f"\nProxies: {PROXY_COSTS['note']}")
    print(f"  Estimated {PROXY_COSTS['typical_gb_per_1k']} GB per 1k records")
    print(f"  Sources: BrightData, Oxylabs, SmartProxy")
    print(f"\nAPIs: {API_COSTS['note']}")
    print(f"  X API Basic tier: ${API_COSTS['x_api_basic']}/month")
    print(f"  Sources: X Developer Platform, Apify documentation")
    print(f"\nAI Enrichment (Optional): {AI_ENRICHMENT_COSTS['note']}")
    print(f"  Avg {AI_ENRICHMENT_COSTS['avg_tokens_per_record']} tokens per record")
    print(f"  Sources: Anthropic and OpenAI pricing pages")
    print("\n" + "="*80 + "\n")


def save_csv_output(results: List[Dict], output_path: Path):
    """Save cost estimates to CSV file."""
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = [
            'Volume',
            'Scraping Min', 'Scraping Max',
            'Proxy Residential Min', 'Proxy Residential Max',
            'Proxy Datacenter Min', 'Proxy Datacenter Max',
            'API Monthly Cost',
            'Total Residential Min', 'Total Residential Max',
            'Total Datacenter Min', 'Total Datacenter Max',
            'Cost per Contact Residential Min', 'Cost per Contact Residential Max',
            'Cost per Contact Datacenter Min', 'Cost per Contact Datacenter Max',
        ]

        # Add AI fields if present
        if 'ai_enrichment_claude' in results[0]:
            fieldnames.extend([
                'AI Claude Min', 'AI Claude Max',
                'AI GPT-4 Min', 'AI GPT-4 Max',
                'Total with Claude Min', 'Total with Claude Max',
                'Total with GPT-4 Min', 'Total with GPT-4 Max',
            ])

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            row = {
                'Volume': result['volume'],
                'Scraping Min': result['scraping_cost'][0],
                'Scraping Max': result['scraping_cost'][1],
                'Proxy Residential Min': result['proxy_cost_residential'][0],
                'Proxy Residential Max': result['proxy_cost_residential'][1],
                'Proxy Datacenter Min': result['proxy_cost_datacenter'][0],
                'Proxy Datacenter Max': result['proxy_cost_datacenter'][1],
                'API Monthly Cost': result['api_cost_monthly'],
                'Total Residential Min': result['total_residential'][0],
                'Total Residential Max': result['total_residential'][1],
                'Total Datacenter Min': result['total_datacenter'][0],
                'Total Datacenter Max': result['total_datacenter'][1],
                'Cost per Contact Residential Min': result['cost_per_contact_residential'][0],
                'Cost per Contact Residential Max': result['cost_per_contact_residential'][1],
                'Cost per Contact Datacenter Min': result['cost_per_contact_datacenter'][0],
                'Cost per Contact Datacenter Max': result['cost_per_contact_datacenter'][1],
            }

            if 'ai_enrichment_claude' in result:
                row.update({
                    'AI Claude Min': result['ai_enrichment_claude'][0],
                    'AI Claude Max': result['ai_enrichment_claude'][1],
                    'AI GPT-4 Min': result['ai_enrichment_gpt4'][0],
                    'AI GPT-4 Max': result['ai_enrichment_gpt4'][1],
                    'Total with Claude Min': result['total_residential_with_claude'][0],
                    'Total with Claude Max': result['total_residential_with_claude'][1],
                    'Total with GPT-4 Min': result['total_residential_with_gpt4'][0],
                    'Total with GPT-4 Max': result['total_residential_with_gpt4'][1],
                })

            writer.writerow(row)

    print(f"CSV output saved to: {output_path}")


def save_markdown_output(results: List[Dict], output_path: Path):
    """Save cost estimates to Markdown file."""
    with open(output_path, 'w') as f:
        f.write("# Cost Estimation Report - Outreach Scraping Toolkit\n\n")
        f.write("*Generated: 2026-02-05*\n\n")

        f.write("## Cost Breakdown by Volume\n\n")

        # Main cost table
        f.write("| Volume | Scraping | Proxy (Residential) | Proxy (Datacenter) | API (Monthly) | Total (Residential) | Total (Datacenter) |\n")
        f.write("|--------|----------|---------------------|-------------------|---------------|---------------------|-------------------|\n")

        for result in results:
            f.write(f"| {result['volume']:,} | ")
            f.write(f"{format_cost_range(result['scraping_cost'])} | ")
            f.write(f"{format_cost_range(result['proxy_cost_residential'])} | ")
            f.write(f"{format_cost_range(result['proxy_cost_datacenter'])} | ")
            f.write(f"${result['api_cost_monthly']:.2f} | ")
            f.write(f"{format_cost_range(result['total_residential'])} | ")
            f.write(f"{format_cost_range(result['total_datacenter'])} |\n")

        # Cost per contact table
        f.write("\n## Cost Per Contact\n\n")
        f.write("| Volume | Residential Proxy | Datacenter Proxy |\n")
        f.write("|--------|-------------------|------------------|\n")

        for result in results:
            f.write(f"| {result['volume']:,} | ")
            f.write(f"{format_cost_range(result['cost_per_contact_residential'])} | ")
            f.write(f"{format_cost_range(result['cost_per_contact_datacenter'])} |\n")

        # AI enrichment table (if applicable)
        if 'ai_enrichment_claude' in results[0]:
            f.write("\n## AI Enrichment Costs (Optional Add-on)\n\n")
            f.write("| Volume | Claude API | GPT-4 API | Total + Claude | Total + GPT-4 |\n")
            f.write("|--------|------------|-----------|----------------|---------------|\n")

            for result in results:
                f.write(f"| {result['volume']:,} | ")
                f.write(f"{format_cost_range(result['ai_enrichment_claude'])} | ")
                f.write(f"{format_cost_range(result['ai_enrichment_gpt4'])} | ")
                f.write(f"{format_cost_range(result['total_residential_with_claude'])} | ")
                f.write(f"{format_cost_range(result['total_residential_with_gpt4'])} |\n")

        # Assumptions and sources
        f.write("\n## Assumptions & Data Sources\n\n")
        f.write("### Scraping Costs\n")
        f.write(f"- {SCRAPING_COSTS['note']}\n")
        f.write(f"- Per 1k records: {format_cost_range(SCRAPING_COSTS['cost_per_1k'])}\n")
        f.write(f"- Per 10k records: {format_cost_range(SCRAPING_COSTS['cost_per_10k'])}\n")
        f.write(f"- Per 50k records: {format_cost_range(SCRAPING_COSTS['cost_per_50k'])}\n")
        f.write("- **Source:** Apify marketplace pricing (https://apify.com/pricing)\n\n")

        f.write("### Proxy Costs\n")
        f.write(f"- {PROXY_COSTS['note']}\n")
        f.write(f"- Residential: {format_cost_range(PROXY_COSTS['residential_per_gb'])} per GB\n")
        f.write(f"- Datacenter: {format_cost_range(PROXY_COSTS['datacenter_per_gb'])} per GB\n")
        f.write(f"- Estimated data usage: {PROXY_COSTS['typical_gb_per_1k']} GB per 1k records\n")
        f.write(f"- Monthly baseline: {format_cost_range(PROXY_COSTS['monthly_baseline'])}\n")
        f.write("- **Sources:** BrightData, Oxylabs, SmartProxy pricing pages\n\n")

        f.write("### API Costs\n")
        f.write(f"- {API_COSTS['note']}\n")
        f.write(f"- LinkedIn: ${API_COSTS['linkedin_via_apify']} (included in Apify costs)\n")
        f.write(f"- X/Twitter API Basic: ${API_COSTS['x_api_basic']}/month\n")
        f.write(f"- X/Twitter API Pro: ${API_COSTS['x_api_pro']}/month\n")
        f.write(f"- X/Twitter API Enterprise: ${API_COSTS['x_api_enterprise']}/month\n")
        f.write("- **Sources:** X Developer Platform, Apify documentation\n\n")

        if 'ai_enrichment_claude' in results[0]:
            f.write("### AI Enrichment Costs (Optional)\n")
            f.write(f"- {AI_ENRICHMENT_COSTS['note']}\n")
            f.write(f"- Claude 3.5 Sonnet: ${AI_ENRICHMENT_COSTS['claude_input_per_1k_tokens']}/1k input tokens, ${AI_ENRICHMENT_COSTS['claude_output_per_1k_tokens']}/1k output tokens\n")
            f.write(f"- GPT-4 Turbo: ${AI_ENRICHMENT_COSTS['gpt4_input_per_1k_tokens']}/1k input tokens, ${AI_ENRICHMENT_COSTS['gpt4_output_per_1k_tokens']}/1k output tokens\n")
            f.write(f"- Estimated {AI_ENRICHMENT_COSTS['avg_tokens_per_record']} tokens per record\n")
            f.write("- **Sources:** Anthropic and OpenAI pricing pages (Jan 2025)\n\n")

        f.write("---\n\n")
        f.write("*This report provides cost estimates based on current market rates. ")
        f.write("Actual costs may vary based on specific requirements, volume discounts, ")
        f.write("and service provider pricing changes.*\n")

    print(f"Markdown output saved to: {output_path}")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main function to run cost estimation analysis."""
    parser = argparse.ArgumentParser(
        description='Cost Estimation Tool for Outreach Scraping Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cost_estimation.py
  python cost_estimation.py --volumes 1000 5000 25000
  python cost_estimation.py --include-ai
  python cost_estimation.py --output-dir ./output
        """
    )

    parser.add_argument(
        '--volumes',
        type=int,
        nargs='+',
        default=[1000, 10000, 50000],
        help='Volume levels to analyze (default: 1000 10000 50000)'
    )

    parser.add_argument(
        '--include-ai',
        action='store_true',
        help='Include AI enrichment costs in analysis'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='./tools',
        help='Output directory for CSV and Markdown files (default: ./tools)'
    )

    args = parser.parse_args()

    # Calculate costs for each volume level
    results = []
    for volume in args.volumes:
        result = calculate_total_cost(volume, include_ai=args.include_ai)
        results.append(result)

    # Print to console
    print_console_output(results)

    # Save outputs
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / 'cost_estimates.csv'
    md_path = output_dir / 'cost_estimates.md'

    save_csv_output(results, csv_path)
    save_markdown_output(results, md_path)

    print("\nCost estimation complete!")
    print(f"Results saved to {output_dir}/")


if __name__ == "__main__":
    main()
