"""
Researcher Agent: Generates search sub-queries, queries DuckDuckGo, scrapes key web pages,
and compiles structured factual insights with citations.
"""
from typing import List, Dict, Any, Callable, Optional
import json
import asyncio
from loguru import logger
from langchain_core.messages import SystemMessage, HumanMessage

from tools.web_search import perform_search
from tools.scraper import scrape_url_async
from utils.llm import get_llm

RESEARCHER_SYSTEM_PROMPT = """You are the Lead Web Researcher of an elite investigative research team.
Your job is to analyze the user's research topic, identify key sub-dimensions (historical context, latest 2025/2026 developments, key technical specs/mechanisms, industry consensus, controversies/risks), and generate 3 to 5 highly focused search queries.

Respond strictly in valid JSON format:
{
  "focus_areas": ["Area 1", "Area 2", "Area 3"],
  "search_queries": ["query 1", "query 2", "query 3", "query 4"]
}
"""

SYNTHESIS_SYSTEM_PROMPT = """You are an expert Research Synthesizer.
Review the collected web search results and scraped webpage excerpts for the topic: "{topic}".

Extract and synthesize the core factual findings into a structured briefing with:
1. Key Factual Findings (with dates, numbers, breakthroughs)
2. Main Players, Companies, or Researchers involved
3. Core Technical/Market Realities
4. Verifiable Claims and Source Citations (URLs and Titles)

Be objective, thorough, and cite URLs for every key claim.
"""

class ResearcherAgent:
    def __init__(self, llm=None):
        self.llm = llm or get_llm()

    async def plan_and_search(
        self,
        topic: str,
        event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """
        Executes complete research workflow:
        1. Formulate search queries
        2. Perform DuckDuckGo searches in parallel
        3. Scrape top candidate web pages
        4. Synthesize raw data into research briefing
        """
        if event_callback:
            await event_callback({
                "agent": "Researcher",
                "stage": "planning",
                "message": f"Analyzing topic and generating targeted search queries for: '{topic}'"
            })

        # Step 1: Formulate search queries
        messages = [
            SystemMessage(content=RESEARCHER_SYSTEM_PROMPT),
            HumanMessage(content=f"Research Topic: {topic}")
        ]
        
        try:
            plan_response = await self.llm.ainvoke(messages)
            content = plan_response.content.strip()
            # Clean possible markdown json wrapper
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            parsed_plan = json.loads(content.strip())
            queries = parsed_plan.get("search_queries", [topic])
        except Exception as e:
            logger.warning(f"Error parsing researcher plan: {e}. Falling back to default queries.")
            queries = [
                topic,
                f"{topic} latest developments analysis",
                f"{topic} pros cons controversy debate",
                f"{topic} key facts research 2025 2026"
            ]

        if event_callback:
            await event_callback({
                "agent": "Researcher",
                "stage": "searching",
                "message": f"Executing {len(queries)} live web searches across DuckDuckGo...",
                "queries": queries
            })

        # Step 2: Perform web searches
        all_search_results = []
        seen_urls = set()
        
        for q in queries:
            results = perform_search(q, max_results=4)
            for r in results:
                url = r.get("url")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_search_results.append(r)

        if event_callback:
            await event_callback({
                "agent": "Researcher",
                "stage": "scraping",
                "message": f"Discovered {len(all_search_results)} relevant web sources. Scraping top pages for deep content...",
                "sources_count": len(all_search_results),
                "sources": all_search_results[:8]
            })

        # Step 3: Scrape top 4 promising URLs
        top_urls = [r["url"] for r in all_search_results[:4] if r.get("url")]
        scrape_tasks = [scrape_url_async(url, max_chars=3000) for url in top_urls]
        scraped_pages = await asyncio.gather(*scrape_tasks, return_exceptions=True)

        scraped_content_snippets = []
        for res in scraped_pages:
            if isinstance(res, dict) and res.get("success") and res.get("text"):
                scraped_content_snippets.append(
                    f"### Page: {res.get('title', 'Unknown')} ({res.get('url')})\n{res.get('text')}\n"
                )

        # Step 4: Synthesize raw research data
        context_block = "\n\n".join([
            f"**Search Result:** {r.get('title')} ({r.get('url')})\nSnippet: {r.get('snippet')}"
            for r in all_search_results[:10]
        ])
        
        if scraped_content_snippets:
            context_block += "\n\n**Deep Web Page Excerpts:**\n" + "\n\n".join(scraped_content_snippets[:3])

        if event_callback:
            await event_callback({
                "agent": "Researcher",
                "stage": "synthesizing",
                "message": "Synthesizing factual evidence, source citations, and key metrics..."
            })

        synthesis_messages = [
            SystemMessage(content=SYNTHESIS_SYSTEM_PROMPT.format(topic=topic)),
            HumanMessage(content=f"Gathered Web Evidence:\n\n{context_block}")
        ]
        
        synthesis_response = await self.llm.ainvoke(synthesis_messages)
        briefing = synthesis_response.content

        return {
            "queries": queries,
            "sources": all_search_results,
            "scraped_count": len(scraped_content_snippets),
            "research_briefing": briefing
        }
