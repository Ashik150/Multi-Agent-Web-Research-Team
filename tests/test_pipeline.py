"""
Unit tests for tools and pipeline components.
"""
import pytest
from tools.web_search import perform_search
from tools.scraper import scrape_url_sync
from graph.research_graph import MultiAgentResearchGraph


def test_web_search():
    results = perform_search("artificial intelligence", max_results=3)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "url" in results[0]
    assert "title" in results[0]


def test_scraper_sync():
    res = scrape_url_sync("https://en.wikipedia.org/wiki/Artificial_intelligence", max_chars=500)
    assert res["success"] is True
    assert "Artificial intelligence" in res["title"] or len(res["text"]) > 50


def test_graph_initialization():
    graph = MultiAgentResearchGraph()
    assert graph.graph is not None
