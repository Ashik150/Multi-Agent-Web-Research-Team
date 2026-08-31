"""
Entry point for the Multi-Agent Web Research system.

Usage:
    python main.py
    python main.py --query "Latest AI breakthroughs in 2025"
"""
import argparse
import sys

from loguru import logger
from rich.console import Console
from rich.panel import Panel

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Web Research Team",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--query",
        "-q",
        type=str,
        default=None,
        help="Research query to investigate (prompted interactively if omitted)",
    )
    args = parser.parse_args()

    console.print(
        Panel.fit(
            "[bold cyan]🤖 Multi-Agent Web Research Team[/bold cyan]\n"
            "[dim]Powered by LangGraph + OpenAI[/dim]",
            border_style="cyan",
        )
    )

    query = args.query or console.input("\n[bold yellow]🔍 Enter research query:[/bold yellow] ").strip()

    if not query:
        console.print("[red]No query provided. Exiting.[/red]")
        sys.exit(1)

    logger.info(f"Starting research for: {query!r}")
    console.print(f"\n[green]▶ Researching:[/green] {query}\n")

    # TODO: wire up the LangGraph research graph here
    # from graph.research_graph import ResearchGraph
    # result = ResearchGraph().run(query)
    console.print("[yellow]⚙  Agents not yet wired up — add your graph in graph/research_graph.py[/yellow]")


if __name__ == "__main__":
    main()
