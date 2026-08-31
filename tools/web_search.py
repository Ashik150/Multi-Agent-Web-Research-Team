"""
Web search tool utilizing DuckDuckGo (via direct DDG Lite parser & DDGS), Tavily, and Wikipedia.
Zero-dependency on external API keys required, works seamlessly across all platforms.
"""
from typing import List, Dict, Any, Optional
from loguru import logger
import os
import re
import urllib.parse
import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def search_duckduckgo_lite(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Direct DuckDuckGo Lite search. Highly resilient, free, and no TLS/LibreSSL incompatibilities.
    """
    results = []
    try:
        url = "https://lite.duckduckgo.com/lite/"
        with httpx.Client(headers=HEADERS, timeout=10.0, follow_redirects=True) as client:
            resp = client.post(url, data={"q": query})
            if resp.status_code != 200:
                return results

            soup = BeautifulSoup(resp.text, "html.parser")
            rows = soup.find_all("tr")
            
            current_title = ""
            current_url = ""
            
            for row in rows:
                link_tag = row.find("a", class_="result-link")
                snippet_tag = row.find("td", class_="result-snippet")
                
                if link_tag:
                    raw_href = link_tag.get("href", "")
                    if "uddg=" in raw_href:
                        current_url = urllib.parse.unquote(raw_href.split("uddg=")[1].split("&")[0])
                    else:
                        current_url = raw_href
                    current_title = link_tag.get_text(strip=True)
                
                elif snippet_tag and current_url and current_title:
                    snippet = snippet_tag.get_text(strip=True)
                    results.append({
                        "title": current_title,
                        "url": current_url,
                        "snippet": snippet,
                        "source": "DuckDuckGo"
                    })
                    current_title = ""
                    current_url = ""
                    
                    if len(results) >= max_results:
                        break
                        
        logger.info(f"DuckDuckGo Lite search for '{query}' returned {len(results)} results")
    except Exception as e:
        logger.warning(f"DuckDuckGo Lite search error for '{query}': {e}")
    return results


def search_wikipedia(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Wikipedia OpenSearch API fallback.
    """
    results = []
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={encoded_query}&limit={max_results}&namespace=0&format=json"
        with httpx.Client(headers=HEADERS, timeout=8.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                titles = data[1] if len(data) > 1 else []
                snippets = data[2] if len(data) > 2 else []
                urls = data[3] if len(data) > 3 else []
                for i in range(len(titles)):
                    results.append({
                        "title": titles[i],
                        "url": urls[i] if i < len(urls) else f"https://en.wikipedia.org/wiki/{urllib.parse.quote(titles[i])}",
                        "snippet": snippets[i] if i < len(snippets) else "",
                        "source": "Wikipedia"
                    })
    except Exception as e:
        logger.debug(f"Wikipedia search error: {e}")
    return results


def search_tavily(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Tavily search fallback if API key exists.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return []
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results)
        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", ""),
                "source": "Tavily"
            })
        return results
    except Exception as e:
        logger.warning(f"Tavily search error: {e}")
        return []


def perform_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Unified search executor across DDG Lite, Tavily, and Wikipedia.
    """
    # 1. Primary: DuckDuckGo Lite
    results = search_duckduckgo_lite(query, max_results=max_results)

    # 2. Secondary: Tavily (if configured and few results)
    if len(results) < 2 and os.getenv("TAVILY_API_KEY"):
        t_results = search_tavily(query, max_results=max_results)
        for tr in t_results:
            if not any(r["url"] == tr["url"] for r in results):
                results.append(tr)

    # 3. Tertiary: Wikipedia
    if len(results) < 2:
        w_results = search_wikipedia(query, max_results=3)
        for wr in w_results:
            if not any(r["url"] == wr["url"] for r in results):
                results.append(wr)

    return results
