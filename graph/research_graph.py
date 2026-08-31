"""
LangGraph Multi-Agent Web Research Workflow.
Orchestrates Researcher, Debater, Writer, and Reviewer agents in a stateful, cyclical graph.
"""
from typing import Dict, Any, List, Optional, Callable, TypedDict, Annotated
import asyncio
from loguru import logger
from langgraph.graph import StateGraph, END

from agents.researcher import ResearcherAgent
from agents.debater import DebaterAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent
from utils.llm import get_llm


class ResearchState(TypedDict, total=False):
    topic: str
    research_queries: List[str]
    sources: List[Dict[str, Any]]
    research_briefing: str
    debate_transcript: str
    draft_report: str
    review_feedback: Dict[str, Any]
    final_report: str
    iteration: int
    max_iterations: int
    event_callback: Optional[Callable[[Dict[str, Any]], None]]


class MultiAgentResearchGraph:
    def __init__(
        self,
        llm=None,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.llm = llm or get_llm(provider=provider, model_name=model_name, api_key=api_key)
        self.researcher = ResearcherAgent(llm=self.llm)
        self.debater = DebaterAgent(llm=self.llm)
        self.writer = WriterAgent(llm=self.llm)
        self.reviewer = ReviewerAgent(llm=self.llm)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(ResearchState)

        # Define Nodes
        workflow.add_node("research", self._research_node)
        workflow.add_node("debate", self._debate_node)
        workflow.add_node("write", self._write_node)
        workflow.add_node("review", self._review_node)
        workflow.add_node("finalize", self._finalize_node)

        # Set Entry Point
        workflow.set_entry_point("research")

        # Define Linear Edges
        workflow.add_edge("research", "debate")
        workflow.add_edge("debate", "write")
        workflow.add_edge("write", "review")

        # Define Conditional Loop
        workflow.add_conditional_edges(
            "review",
            self._route_after_review,
            {
                "revise": "write",
                "finalize": "finalize",
            }
        )

        workflow.add_edge("finalize", END)
        return workflow.compile()

    async def _research_node(self, state: ResearchState) -> Dict[str, Any]:
        topic = state["topic"]
        callback = state.get("event_callback")
        res = await self.researcher.plan_and_search(topic, event_callback=callback)
        return {
            "research_queries": res["queries"],
            "sources": res["sources"],
            "research_briefing": res["research_briefing"],
            "iteration": state.get("iteration", 0) + 1,
            "max_iterations": state.get("max_iterations", 2),
        }

    async def _debate_node(self, state: ResearchState) -> Dict[str, Any]:
        topic = state["topic"]
        briefing = state.get("research_briefing", "")
        callback = state.get("event_callback")
        res = await self.debater.conduct_debate(topic, briefing, event_callback=callback)
        return {
            "debate_transcript": res["debate_transcript"]
        }

    async def _write_node(self, state: ResearchState) -> Dict[str, Any]:
        topic = state["topic"]
        briefing = state.get("research_briefing", "")
        debate = state.get("debate_transcript", "")
        sources = state.get("sources", [])
        review_fb = state.get("review_feedback", {})
        feedback_text = review_fb.get("critical_feedback") if review_fb.get("needs_revision") else None
        callback = state.get("event_callback")

        res = await self.writer.draft_report(
            topic=topic,
            research_briefing=briefing,
            debate_transcript=debate,
            sources=sources,
            revision_feedback=feedback_text,
            event_callback=callback,
        )
        return {
            "draft_report": res["draft_report"]
        }

    async def _review_node(self, state: ResearchState) -> Dict[str, Any]:
        topic = state["topic"]
        draft = state.get("draft_report", "")
        iteration = state.get("iteration", 1)
        max_iterations = state.get("max_iterations", 2)
        callback = state.get("event_callback")

        review_res = await self.reviewer.review_draft(
            topic=topic,
            draft_report=draft,
            iteration=iteration,
            max_iterations=max_iterations,
            event_callback=callback,
        )
        return {
            "review_feedback": review_res
        }

    def _route_after_review(self, state: ResearchState) -> str:
        review_fb = state.get("review_feedback", {})
        iteration = state.get("iteration", 1)
        max_iterations = state.get("max_iterations", 2)

        if review_fb.get("needs_revision") and iteration < max_iterations:
            logger.info(f"Routing to Revision (Iteration {iteration}/{max_iterations})")
            return "revise"
        return "finalize"

    async def _finalize_node(self, state: ResearchState) -> Dict[str, Any]:
        topic = state["topic"]
        draft = state.get("draft_report", "")
        review_fb = state.get("review_feedback", {})
        review_notes = review_fb.get("critical_feedback", "Approved")
        callback = state.get("event_callback")

        final_content = await self.reviewer.polish_and_finalize(
            topic=topic,
            draft_report=draft,
            review_notes=review_notes,
            event_callback=callback,
        )

        if callback:
            await callback({
                "agent": "Orchestrator",
                "stage": "complete",
                "message": "🎉 Multi-agent research complete! Final report ready.",
                "final_report": final_content,
                "sources": state.get("sources", []),
                "debate": state.get("debate_transcript", ""),
                "review": review_fb,
            })

        return {
            "final_report": final_content
        }

    async def arun(
        self,
        topic: str,
        max_iterations: int = 2,
        event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """
        Execute the full multi-agent pipeline asynchronously.
        """
        initial_state: ResearchState = {
            "topic": topic,
            "max_iterations": max_iterations,
            "iteration": 0,
            "event_callback": event_callback,
        }
        return await self.graph.ainvoke(initial_state)
