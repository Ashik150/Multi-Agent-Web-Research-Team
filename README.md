# Multi-Agent Web Research Team 🤖🔍

A multi-agent AI system built with **LangGraph** for autonomous web research, information synthesis, and report generation.

## 🗂️ Project Structure

```
Multi-Agent Web Research Team/
├── agents/              # Individual agent definitions
│   ├── __init__.py
│   ├── researcher.py    # Web search & data collection agent
│   ├── analyst.py       # Information synthesis agent
│   └── writer.py        # Report generation agent
├── tools/               # Custom tools for agents
│   ├── __init__.py
│   ├── web_search.py    # Tavily / DuckDuckGo search
│   └── scraper.py       # Web page scraping
├── graph/               # LangGraph workflow definitions
│   ├── __init__.py
│   └── research_graph.py
├── utils/               # Shared utilities
│   ├── __init__.py
│   └── config.py
├── tests/               # Unit and integration tests
├── .env.example         # API key template → copy to .env
├── requirements.txt
└── main.py              # Entry point
```

## 🚀 Quick Start

```bash
# 1. Activate the virtual environment
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and fill in your API keys
cp .env.example .env

# 4. Run the research agent
python main.py
```

## 🔑 Required API Keys

| Key | Used For | Get It |
|-----|----------|--------|
| `OPENAI_API_KEY` | LLM backbone | [platform.openai.com](https://platform.openai.com) |
| `TAVILY_API_KEY` | Web search | [tavily.com](https://tavily.com) |
| `LANGCHAIN_API_KEY` | LangSmith tracing *(optional)* | [smith.langchain.com](https://smith.langchain.com) |

## 🧩 Tech Stack

- **[LangGraph](https://langchain-ai.github.io/langgraph/)** — stateful multi-agent orchestration
- **[LangChain](https://python.langchain.com/)** — LLM tools, chains, and memory
- **[Tavily](https://tavily.com/)** — real-time web search API for agents
- **[OpenAI](https://openai.com/)** — GPT-4o as the agent LLM
- **[Rich](https://rich.readthedocs.io/)** — beautiful terminal output
- **[Loguru](https://loguru.readthedocs.io/)** — structured logging
