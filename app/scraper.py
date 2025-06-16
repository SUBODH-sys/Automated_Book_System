import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_content(url, output_dir="data/content", screenshot_dir="data/screenshots"):
    """
    Scrape content from a URL and save screenshots using Playwright.
    Extract plain text using BeautifulSoup.
    """
    try:
        # Create directories if they don't exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Initialize Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)  # Set timeout to 60 seconds
            
            # Save HTML content
            html_content = page.content()
            html_path = os.path.join(output_dir, "chapter1.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # Save screenshot
            screenshot_path = os.path.join(screenshot_dir, "chapter1.png")
            page.screenshot(path=screenshot_path, full_page=True)
            
            browser.close()
        
        # Extract plain text
        soup = BeautifulSoup(html_content, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        text_path = os.path.join(output_dir, "chapter1.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        return text
    
    except Exception as e:
        raise Exception(f"Scraping failed: {str(e)}")