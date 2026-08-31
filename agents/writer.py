"""
Writer Agent: Synthesizes research evidence, debate outcomes, and facts into an extensive,
publication-grade Markdown report with rich formatting, tables, and citations.
"""
from typing import Dict, Any, Callable, Optional, List
from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm

WRITER_SYSTEM_PROMPT = """You are an elite Senior Research Author and Technical Writer.
Your task is to write a comprehensive, exhaustive, publication-grade research report on the topic: "{topic}".

Inputs available to you:
- **Research Evidence & Fact Briefing**:
{briefing}

- **Multi-Perspective Debate & Tradeoffs**:
{debate}

- **Verified Web Sources & Citations**:
{sources_list}

{revision_notes}

### Writing Guidelines:
1. **Title**: Catchy, clear, authoritative title.
2. **Executive Summary**: High-level abstract highlighting the bottom line.
3. **Core Themes & Technological/Market Deep Dive**: Thorough analysis with sub-headings (`###`), bullet points, and data tables where helpful.
4. **Debate & Strategic Trade-offs**: Incorporate the competing arguments (optimistic possibilities vs realistic bottlenecks/risks).
5. **Future Outlook & Strategic Recommendations**: Actionable conclusions for practitioners/decision-makers.
6. **Sources & References**: List all cited URLs with markdown hyperlinks `[Source Title](URL)`.

Make the report engaging, deeply informative, and styled with professional Markdown (tables, blockquotes, bold key terms). Do NOT include meta commentary like "Here is the report:".
"""

class WriterAgent:
    def __init__(self, llm=None):
        self.llm = llm or get_llm()

    async def draft_report(
        self,
        topic: str,
        research_briefing: str,
        debate_transcript: str,
        sources: List[Dict[str, Any]],
        revision_feedback: Optional[str] = None,
        event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """
        Drafts or revises the final research report.
        """
        is_revision = bool(revision_feedback)
        
        if event_callback:
            await event_callback({
                "agent": "Writer",
                "stage": "revising" if is_revision else "drafting",
                "message": (
                    "Revising report incorporating Reviewer feedback..."
                    if is_revision
                    else "Drafting comprehensive research report with synthesized data and debate points..."
                )
            })

        sources_text = "\n".join([
            f"- [{s.get('title', 'Web Source')}]({s.get('url', '#')}): {s.get('snippet', '')[:120]}..."
            for s in sources if s.get("url")
        ])

        revision_block = ""
        if revision_feedback:
            revision_block = f"\n### Editorial Reviewer Feedback to address in this revision:\n{revision_feedback}\n"

        prompt = WRITER_SYSTEM_PROMPT.format(
            topic=topic,
            briefing=research_briefing,
            debate=debate_transcript,
            sources_list=sources_text,
            revision_notes=revision_block
        )

        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content="Please write the full, comprehensive Markdown report now.")
        ]

        response = await self.llm.ainvoke(messages)
        report_content = response.content

        if event_callback:
            await event_callback({
                "agent": "Writer",
                "stage": "draft_complete",
                "message": f"Draft completed ({len(report_content.split())} words). Handing over to Reviewer...",
                "word_count": len(report_content.split())
            })

        return {
            "draft_report": report_content
        }
