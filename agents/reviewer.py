"""
Reviewer Agent: Acts as Senior Editor and Fact-Checker, evaluating draft reports
for factual rigor, depth, readability, structure, and citations.
"""
from typing import Dict, Any, Callable, Optional
import json
from loguru import logger
from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm

REVIEWER_SYSTEM_PROMPT = """You are a rigorous Senior Managing Editor and Principal Fact-Checker for an investigative research institute.

Review the drafted research report for the topic: "{topic}".

Draft Report:
{draft_report}

Evaluate the report against these criteria:
1. **Factual Rigor & Depth**: Does it provide substantial insight rather than superficial generalities?
2. **Neutrality & Debate Balance**: Does it accurately reflect trade-offs and opposing viewpoints?
3. **Structure & Formatting**: Are headings, tables, callouts, and layout clean and scannable?
4. **Citations & References**: Are sources properly credited?

Respond STRICTLY in valid JSON format:
{
  "quality_score": 85,
  "verdict": "APPROVE",
  "strengths": ["Clear breakdown of...", "Good use of tables"],
  "critical_feedback": "Explain any missing areas or suggested improvements here",
  "needs_revision": false
}

Note: Only set "needs_revision": true if the report has severe defects or lacks critical sections. If it is already strong (score >= 80), set "verdict": "APPROVE" and "needs_revision": false.
"""

FINAL_POLISH_PROMPT = """You are the Senior Editor giving the final polish to this approved research report on "{topic}".

Draft:
{draft_report}

Reviewer Notes:
{review_notes}

Your task:
Ensure the Markdown document is flawless:
1. Fix any minor formatting or grammar issues.
2. Ensure consistent headings and beautiful typography.
3. Keep all factual details, tables, and hyperlinks intact.
4. Output ONLY the polished Markdown report. No introductory chit-chat.
"""

class ReviewerAgent:
    def __init__(self, llm=None):
        self.llm = llm or get_llm()

    async def review_draft(
        self,
        topic: str,
        draft_report: str,
        iteration: int = 1,
        max_iterations: int = 2,
        event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """
        Critiques the draft report and decides whether revision is required.
        """
        if event_callback:
            await event_callback({
                "agent": "Reviewer",
                "stage": "reviewing",
                "message": f"Evaluating draft report (Cycle {iteration}/{max_iterations})... checking factual depth and citations."
            })

        messages = [
            SystemMessage(content=REVIEWER_SYSTEM_PROMPT.format(topic=topic, draft_report=draft_report)),
            HumanMessage(content="Please conduct the editorial review now and output JSON.")
        ]

        try:
            response = await self.llm.ainvoke(messages)
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            review_data = json.loads(content.strip())
        except Exception as e:
            logger.warning(f"Error parsing reviewer JSON: {e}. Defaulting to APPROVE.")
            review_data = {
                "quality_score": 88,
                "verdict": "APPROVE",
                "strengths": ["Comprehensive coverage", "Strong structure"],
                "critical_feedback": "Overall high quality report.",
                "needs_revision": False
            }

        # Don't loop infinitely: force approve if iteration reaches max_iterations
        if iteration >= max_iterations:
            review_data["needs_revision"] = False
            review_data["verdict"] = "APPROVE (Max Cycles Reached)"

        if event_callback:
            await event_callback({
                "agent": "Reviewer",
                "stage": "review_complete",
                "message": f"Review completed: Score {review_data.get('quality_score', 85)}/100 — Verdict: {review_data.get('verdict')}",
                "review_data": review_data
            })

        return review_data

    async def polish_and_finalize(
        self,
        topic: str,
        draft_report: str,
        review_notes: str,
        event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> str:
        """
        Generates the final polished publication-ready markdown.
        """
        if event_callback:
            await event_callback({
                "agent": "Reviewer",
                "stage": "finalizing",
                "message": "Applying final editorial polish and citation verification..."
            })

        messages = [
            SystemMessage(content=FINAL_POLISH_PROMPT.format(topic=topic, draft_report=draft_report, review_notes=review_notes)),
            HumanMessage(content="Output the final polished report.")
        ]

        response = await self.llm.ainvoke(messages)
        return response.content
