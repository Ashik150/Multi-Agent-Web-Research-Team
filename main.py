"""
Multi-Agent Web Research Team - Entry Point

Usage:
    # 1. Launch Web App (Backend API + Web Dashboard):
    python main.py --server

    # 2. Interactive CLI Mode:
    python main.py

    # 3. Direct Query CLI:
    python main.py --query "Quantum Computing progress in 2026"
"""
import argparse
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from loguru import logger

console = Console()


async def run_cli_research(query: str, provider: str = "groq", model: str = None):
    from graph.research_graph import MultiAgentResearchGraph
    
    console.print(Panel.fit(
        f"[bold cyan]🔍 Research Topic:[/bold cyan] {query}\n"
        f"[dim]Provider: {provider} | Model: {model or 'default'}[/dim]",
        border_style="cyan"
    ))

    async def event_callback(event: dict):
        agent = event.get("agent", "Agent")
        stage = event.get("stage", "")
        message = event.get("message", "")

        color_map = {
            "Researcher": "cyan",
            "Debater": "yellow",
            "Writer": "magenta",
            "Reviewer": "green",
            "Orchestrator": "bold white",
            "System": "blue",
        }
        color = color_map.get(agent, "white")

        if stage == "searching" and "queries" in event:
            console.print(f"[{color}][{agent}][/{color}] {message}")
            for q in event.get("queries", []):
                console.print(f"   [dim]• Search Query:[/dim] [cyan]{q}[/cyan]")
        elif stage == "scraping" and "sources" in event:
            console.print(f"[{color}][{agent}][/{color}] {message}")
            for s in event.get("sources", [])[:3]:
                console.print(f"   [dim]• Source:[/dim] [green]{s.get('title')}[/green] ({s.get('url')})")
        elif stage == "review_complete" and "review_data" in event:
            rd = event["review_data"]
            console.print(f"[{color}][{agent}][/{color}] Score: [bold]{rd.get('quality_score')}/100[/bold] — Verdict: [bold green]{rd.get('verdict')}[/bold green]")
        else:
            console.print(f"[{color}][{agent}][/{color}] {message}")

    graph = MultiAgentResearchGraph(provider=provider, model_name=model)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Agents collaborating...", total=None)
        result = await graph.arun(topic=query, event_callback=event_callback)

    final_report = result.get("final_report", "")
    if final_report:
        console.print("\n" + "=" * 80 + "\n")
        console.print(Panel("[bold green]🏆 FINAL RESEARCH REPORT[/bold green]", border_style="green"))
        console.print(Markdown(final_report))
        
        # Save to file
        safe_name = "".join(c if c.isalnum() else "_" for c in query)[:40]
        output_file = Path(__file__).parent / f"report_{safe_name}.md"
        output_file.write_text(final_report, encoding="utf-8")
        console.print(f"\n[bold green]💾 Report saved to:[/bold green] {output_file.resolve()}\n")
    else:
        console.print("[red]❌ Research did not generate a final report.[/red]")


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Web Research Team (LangGraph + Groq/OpenAI + DuckDuckGo)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--server",
        "--serve",
        action="store_true",
        help="Launch the FastAPI server + Web Frontend (default port: 8000)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Server host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--query",
        "-q",
        type=str,
        default=None,
        help="Research query (runs in CLI mode)",
    )
    parser.add_argument(
        "--provider",
        "-p",
        type=str,
        default="groq",
        choices=["groq", "openai", "gemini", "anthropic"],
        help="LLM provider (default: groq)",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help="Specific model name (optional)",
    )

    args = parser.parse_args()

    if args.server:
        console.print(Panel.fit(
            f"[bold cyan]🚀 Launching Multi-Agent Web Research Server[/bold cyan]\n"
            f"[green]URL:[/green] http://localhost:{args.port}\n"
            f"[dim]API Docs: http://localhost:{args.port}/docs[/dim]",
            border_style="cyan"
        ))
        import uvicorn
        uvicorn.run("server:app", host=args.host, port=args.port, reload=True)
    else:
        console.print(Panel.fit(
            "[bold cyan]🤖 Multi-Agent Web Research Team[/bold cyan]\n"
            "[dim]LangGraph • Groq / OpenAI • DuckDuckGo Live Web Search[/dim]",
            border_style="cyan",
        ))
        query = args.query
        if not query:
            query = console.input("\n[bold yellow]🔍 Enter research topic/question:[/bold yellow] ").strip()
        
        if not query:
            console.print("[red]No query provided. Exiting.[/red]")
            sys.exit(1)

        asyncio.run(run_cli_research(query=query, provider=args.provider, model=args.model))


if __name__ == "__main__":
    main()
