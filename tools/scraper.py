"""
Web scraper tool for extracting cleaned, readable text content from web pages.
"""
import re
from typing import Optional, Dict, Any
import httpx
from bs4 import BeautifulSoup
from loguru import logger

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def clean_html(html: str) -> str:
    """Extract readable text from HTML by removing scripts, styles, and boilerplate."""
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove unwanted tags
    for element in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "button"]):
        element.extract()
        
    # Get text
    text = soup.get_text(separator="\n")
    
    # Clean whitespace and empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = "\n".join(lines)
    
    # Remove excessive blank lines or repeats
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)
    return cleaned_text


async def scrape_url_async(url: str, max_chars: int = 4000, timeout: float = 10.0) -> Dict[str, Any]:
    """
    Fetch and scrape a URL asynchronously.
    Returns dict with url, title, text, and success status.
    """
    try:
        async with httpx.AsyncClient(headers=DEFAULT_HEADERS, follow_redirects=True, timeout=timeout) as client:
            response = await client.get(url)
            if response.status_code != 200:
                return {"url": url, "text": "", "title": "", "error": f"HTTP {response.status_code}", "success": False}
            
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            
            text = clean_html(html)
            if len(text) > max_chars:
                text = text[:max_chars] + "... [Content truncated for length]"
                
            return {
                "url": url,
                "title": title,
                "text": text,
                "success": True
            }
    except Exception as e:
        logger.debug(f"Failed to scrape {url}: {e}")
        return {"url": url, "text": "", "title": "", "error": str(e), "success": False}


def scrape_url_sync(url: str, max_chars: int = 4000, timeout: float = 10.0) -> Dict[str, Any]:
    """
    Synchronous version of URL scraper.
    """
    try:
        with httpx.Client(headers=DEFAULT_HEADERS, follow_redirects=True, timeout=timeout) as client:
            response = client.get(url)
            if response.status_code != 200:
                return {"url": url, "text": "", "title": "", "error": f"HTTP {response.status_code}", "success": False}
            
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            
            text = clean_html(html)
            if len(text) > max_chars:
                text = text[:max_chars] + "... [Content truncated for length]"
                
            return {
                "url": url,
                "title": title,
                "text": text,
                "success": True
            }
    except Exception as e:
        logger.debug(f"Failed to scrape {url}: {e}")
        return {"url": url, "text": "", "title": "", "error": str(e), "success": False}
