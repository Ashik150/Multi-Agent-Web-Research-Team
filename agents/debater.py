"""
Debater Agent: Orchestrates a multi-perspective debate (Advocate, Skeptic, Synthesizer)
to challenge assumptions, analyze trade-offs, and produce nuanced insights.
"""
from typing import Dict, Any, Callable, Optional, List
from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm

DEBATE_PROMPT = """You are conducting an intellectual round-table debate among three specialized personas on the research topic: "{topic}".

Evidence & Research Briefing:
{briefing}

The Personas:
1. **The Advocate / Optimist** 🟢: Emphasizes opportunities, bullish arguments, breakthroughs, economic/technological potential, and why this matters positively.
2. **The Skeptic / Critic** 🔴: Challenges hype, identifies blind spots, vulnerabilities, ethical/financial/technical risks, unproven claims, and failure modes.
3. **The Pragmatic Analyst / Moderator** ⚖️: Weighs both sides, identifies consensus facts vs speculative claims, outlines concrete trade-offs, and proposes a balanced conclusion.

Format your output as an engaging multi-round debate with clear persona headers, followed by a **Debate Consensus & Key Tradeoffs** summary.
"""

class DebaterAgent:
    def __init__(self, llm=None):
        self.llm = llm or get_llm()

    async def conduct_debate(
        self,
        topic: str,
        research_briefing: str,
        event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """
        Conducts a multi-perspective debate on the topic using gathered research.
        """
        if event_callback:
            await event_callback({
                "agent": "Debater",
                "stage": "starting_debate",
                "message": "Initiating multi-persona intellectual debate (Advocate vs. Skeptic vs. Pragmatist)..."
            })

        messages = [
            SystemMessage(content=DEBATE_PROMPT.format(topic=topic, briefing=research_briefing)),
            HumanMessage(content="Please conduct the structured debate now based on the briefing.")
        ]

        response = await self.llm.ainvoke(messages)
        debate_text = response.content

        if event_callback:
            await event_callback({
                "agent": "Debater",
                "stage": "debate_completed",
                "message": "Debate completed. Core arguments and tradeoffs identified.",
                "debate_preview": debate_text[:300] + "..."
            })

        return {
            "debate_transcript": debate_text
        }
