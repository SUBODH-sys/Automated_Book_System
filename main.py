from app.scraper import scrape_content
from app.ai_processor import spin_content, review_content
from app.storage import save_version
from app.search import search_versions
from dotenv import load_dotenv
import os

def run_workflow(url):
    """
    Run the complete book publication workflow.
    """
    try:
        # Step 1: Scrape content
        print("Scraping content...")
        text = scrape_content(url)
        save_version("original", text, "original")
        print("Original content saved.")
        
        # Step 2: AI Spin
        print("Spinning content...")
        spun_text = spin_content(text)
        save_version("ai_spun", spun_text, "ai_spun")
        print("AI-spun content saved.")
        
        # Step 3: AI Review
        print("Reviewing content...")
        reviewed_text, review_note = review_content(spun_text)
        save_version("ai_reviewed", reviewed_text, "ai_reviewed")
        print(f"AI-reviewed content saved. Review notes: {review_note}")
        
        # Step 4: Human Review (via Streamlit)
        print("Run `streamlit run app/human_review.py` for human editing.")
        
        # Step 5: Search demo
        print("Searching for latest versions...")
        results = search_versions("latest chapter version")
        for result in results:
            print(f"Version: {result['metadata']['version']}\nContent: {result['document'][:200]}...\n")
    
    except Exception as e:
        print(f"Workflow failed: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    url = os.getenv("SOURCE_URL", "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1")
    run_workflow(url)