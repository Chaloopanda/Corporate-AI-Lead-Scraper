"""
Corporate Remote AI Lead Scraper
================================

Prerequisites & Installation:
-----------------------------
Before running this script, ensure you have Python 3 installed.
You need to install the following dependencies using pip:

    pip install requests beautifulsoup4 pandas tabulate

How to Run:
-----------
1. Modify the `target_urls` list in the `main()` function with the actual profile URLs you want to scrape.
2. Run the script from your terminal:
   
    python lead_scraper.py

3. The script will generate a 'corporate_remote_leads.md' file in the same directory.
"""

import time
import random
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of common user agents to rotate and prevent blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
]

# Technical keywords for publications and projects
TECHNICAL_KEYWORDS = [
    "Vision Transformers", "ViT", "Generative Adversarial Networks", "GANs",
    "Algorithmic Fairness", "Demographic Parity", "Trustworthy AI", "Bias Mitigation",
    "Tensor Networks", "Tensor Train", "Matrix Product States", "Quantum-Inspired ML",
    "Affective Computing", "Facial Emotion Recognition", "FER",
    "Computer Vision", "Surveillance", "High-Resolution Imagery", "Edge AI"
]

# Keywords for checking affiliation type
CORPORATE_LAB_KEYWORDS = [
    "microsoft", "adobe", "google", "meta", "facebook", "apple", "amazon", 
    "nvidia", "deepmind", "openai", "research lab", "startup", "inc", "llc", "corp"
]

# Keywords for checking remote/location feasibility
REMOTE_KEYWORDS = ["remote", "distributed", "global", "india", "wfh", "anywhere"]

# Keywords for internship potential
INTERNSHIP_KEYWORDS = ["intern", "internship", "undergraduate", "student", "b.tech", "bachelors"]

def get_random_headers():
    """Returns a dictionary of headers with a random User-Agent."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

def extract_email(text):
    """
    Extracts email from text using regex.
    Handles standard formats and common obfuscations like name [at] domain [dot] com.
    """
    # Standard email regex
    email_regex = r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
    # Regex for obfuscated emails (e.g., user [at] domain dot com)
    obfuscated_regex = r'([a-zA-Z0-9._-]+(?:\s*\[at\]\s*|\s*\(at\)\s*|\s*@\s*)[a-zA-Z0-9._-]+(?:\s*\[dot\]\s*|\s*\(dot\)\s*|\s*\.\s*)[a-zA-Z0-9_-]+)'
    
    # Try standard first
    match = re.search(email_regex, text)
    if match:
        return match.group(1)
    
    # Try obfuscated
    match = re.search(obfuscated_regex, text, re.IGNORECASE)
    if match:
        cleaned = re.sub(r'\s*\[at\]\s*|\s*\(at\)\s*', '@', match.group(1), flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*\[dot\]\s*|\s*\(dot\)\s*', '.', cleaned, flags=re.IGNORECASE)
        return cleaned.strip()
    
    return "Not Found"

def check_keywords(text, keyword_list):
    """
    Checks if any keyword from the list exists in the text.
    Returns a tuple: (True/False, Matched_Keyword_String_or_None)
    """
    if not text:
        return False, None
    text_lower = text.lower()
    for keyword in keyword_list:
        if keyword.lower() in text_lower:
            return True, keyword
    return False, None

def analyze_profile(url):
    """
    Fetches and parses a profile URL to extract researcher information.
    Includes try-except blocks for robust network request handling.
    """
    print(f"Scraping: {url}")
    try:
        # Network request with timeout and randomized headers
        response = requests.get(url, headers=get_random_headers(), timeout=15)
        response.raise_for_status()
        
        # Respectful scraping delay to prevent IP blocking
        time.sleep(random.uniform(2.0, 4.0))
        
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text(separator=' ', strip=True)
        
        # 1. Name Extraction (Heuristic approach)
        name = "Unknown"
        h1_tag = soup.find('h1')
        if h1_tag:
            name = h1_tag.get_text(strip=True)
        else:
            title_tag = soup.find('title')
            if title_tag:
                name = title_tag.get_text(strip=True).split('|')[0].strip()
                
        # 2. Affiliation
        is_corporate, corporate_kw = check_keywords(page_text, CORPORATE_LAB_KEYWORDS)
        affiliation = "Corporate Lab / Startup" if is_corporate else "University / Other"
        
        # 3. Email Extraction
        email = extract_email(page_text)
        
        # 4. Location / Work Model
        is_remote, remote_kw = check_keywords(page_text, REMOTE_KEYWORDS)
        work_model = f"Remote/Distributed ({remote_kw})" if is_remote else "On-Site / Unspecified"
        
        # 4b. Internship Potential
        is_internship, intern_kw = check_keywords(page_text, INTERNSHIP_KEYWORDS)
        internship_match = f"Yes ({intern_kw})" if is_internship else "No"
        
        # 5. Publication & Project Filtering
        matched_paper = "None"
        matched_keyword = "None"
        has_tech_keyword = False
        
        # Scan typical elements that might contain publications/projects
        potential_items = soup.find_all(['p', 'li', 'div', 'h2', 'h3'])
        
        for item in potential_items:
            item_text = item.get_text(strip=True)
            # Skip noise (too short) or overly large blocks
            if len(item_text) < 15 or len(item_text) > 800:
                continue
                
            has_kw, kw_found = check_keywords(item_text, TECHNICAL_KEYWORDS)
            if has_kw:
                has_tech_keyword = True
                # Truncate long descriptions for the table
                matched_paper = item_text[:120] + "..." if len(item_text) > 120 else item_text
                matched_keyword = kw_found
                break
                
        # 6. Condition & Scoring
        score = 0
        if has_tech_keyword: score += 1
        if is_corporate: score += 1
        if is_remote: score += 1
        if is_internship: score += 1
        
        if score >= 3:
            lead_status = "Tier 1 (Hot Match)"
        elif score >= 1:
            lead_status = "Tier 2"
        else:
            lead_status = "Cold"
            
        return {
            "Name": name,
            "Affiliation": affiliation,
            "Email": email,
            "Lead Status": lead_status,
            "Work Model": work_model,
            "Internship Match": internship_match,
            "Matched Paper/Project": matched_paper,
            "Matched Keyword": matched_keyword,
            "Profile Link": url,
            "Score": score
        }

    except requests.exceptions.RequestException as e:
        print(f"Network error scraping {url}: {e}")
    except Exception as e:
        print(f"Unexpected error scraping {url}: {e}")
        
    # Return a fallback dictionary on error so the script doesn't crash
    return {
        "Name": "Error",
        "Affiliation": "Error",
        "Email": "Error",
        "Lead Status": "Error",
        "Work Model": "Error",
        "Internship Match": "Error",
        "Matched Paper/Project": "Error",
        "Matched Keyword": "Error",
        "Profile Link": url,
        "Score": -1
    }

def main():
    # Provide a list of URLs pointing to specific researcher profiles
    target_urls = [
        "https://www.microsoft.com/en-us/research/people/", # Replace with specific profile URL
        "https://research.adobe.com/person/",               # Replace with specific profile URL
        # Add more target URLs here
    ]
    
    print("Starting AI Researcher Lead Scraper...")
    print(f"Found {len(target_urls)} URLs to process.\n")
    
    results = []
    for url in target_urls:
        data = analyze_profile(url)
        results.append(data)
        
    # Process results into a DataFrame
    df = pd.DataFrame(results)
    
    if not df.empty:
        # Sort by Score descending (Tier 1 at top)
        df = df.sort_values(by="Score", ascending=False)
        
        # Drop the score column for the final markdown output
        df = df.drop(columns=["Score"])
        
        # Export to Markdown
        output_file = "corporate_remote_leads.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Corporate & Remote AI Researcher Leads\n\n")
            # Convert to markdown, ensuring a clean readable format without indices
            f.write(df.to_markdown(index=False))
            
        print(f"\nScraping complete! Results successfully saved to {output_file}")
    else:
        print("\nNo results were gathered.")

if __name__ == "__main__":
    main()
