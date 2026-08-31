# Multi-Agent Web Research Team 🤖🔍

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite%20%2B%20Tailwind-61DAFB.svg)](https://vitejs.dev/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Cloud%20%7C%20OpenAI-F55036.svg)](https://groq.com/)

An autonomous, API-driven Multi-Agent Research Team that collaborates to browse the live web, debate topics from opposing perspectives, and synthesize comprehensive publication-ready Markdown research reports.

---

## 🌟 The Multi-Agent Architecture

```
                                  [ User Query ]
                                        │
                                        ▼
               ┌──────────────────────────────────────────────────┐
               │         LangGraph Orchestration Pipeline         │
               │                                                  │
               │   1. 🔍 Researcher Agent                         │
               │      • Breaks down topic into targeted queries   │
               │      • Scrapes DuckDuckGo live web & extracts   │
               │        citations, numbers, and key facts         │
               │                        │                         │
               │                        ▼                         │
               │   2. ⚡ Debate Engine                            │
               │      • Advocate (Opportunities & Breakthroughs)  │
               │      • Skeptic (Blind spots, Risks & Bottlenecks)│
               │      • Pragmatist (Consensus & Trade-offs)       │
               │                        │                         │
               │                        ▼                         │
               │   3. ✍️ Writer Agent                            │
               │      • Comprehensive publication report drafter  │
               │      • Executive summary, tables, references     │
               │                        │                         │
               │                        ▼                         │
               │   4. 🧐 Reviewer Agent (Managing Editor)         │
               │      • Fact-checker & Rigor evaluator (Score/100)│
               │      • Loops back for revision if score < 80     │
               │                        │                         │
               │                        ▼                         │
               │   5. 🏆 Final Polish & Citation Generator        │
               └──────────────────────────────────────────────────┘
                                        │
                   ┌────────────────────┴────────────────────┐
                   ▼                                         ▼
         🖥️ Modern Web UI (SSE Stream)            💻 Terminal CLI Mode
```

---

## 🚀 Quick Start

### 1. Clone and Setup Environment

```bash
git clone https://github.com/Ashik150/Multi-Agent-Web-Research-Team.git
cd "Multi-Agent Web Research Team"

# Activate Virtual Environment
source .venv/bin/activate
```

### 2. Configure API Keys

```bash
cp .env.example .env
```
Edit `.env` and add your **Groq API Key** (Free & Ultra Fast at [console.groq.com](https://console.groq.com)) or **OpenAI API Key**:
```ini
GROQ_API_KEY=gsk_your_groq_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

> **Note:** Live web search via DuckDuckGo works **100% free with zero API keys required**.

---

## 🎯 Running the Project

### Option A: Launch Full-Stack Web App (Recommended)

```bash
python main.py --server
```
Visit **[http://localhost:8000](http://localhost:8000)** in your browser!

Features of the Web Dashboard:
- ⚡ **Live Real-time SSE Streaming**: Watch each agent think, search the web, and deliberate live.
- 💬 **Interactive Debate Feed**: See the Advocate vs. Skeptic personas debate the topic before drafting.
- 📊 **Step Tracker**: Visual pipeline progress indicators.
- 📝 **Report Viewer**: Markdown renderer, copy to clipboard, download `.md`, print/PDF export, and source links.
- ⚙️ **In-App Model Switcher**: Swap between Groq (LLaMA 3.3 70B), OpenAI (GPT-4o), Claude, or Gemini on the fly.
- 🕒 **Research History**: Saved research sessions in local storage.

### Option B: Run via CLI

```bash
# Interactive Prompt
python main.py

# Direct Query
python main.py --query "Quantum Computing breakthroughs in 2026"

# Specify Provider
python main.py --query "Solid State Batteries commercialization" --provider groq --model llama-3.3-70b-versatile
```

---

## 📁 Project Structure

```
Multi-Agent Web Research Team/
├── agents/                      # AI Agent implementations
│   ├── researcher.py            # Web search, live scraping & fact synthesis
│   ├── debater.py               # Multi-perspective debate engine
│   ├── writer.py                # Publication Markdown report writer
│   └── reviewer.py              # Editorial review, scoring & polish
├── tools/                       # Live tools
│   ├── web_search.py            # DuckDuckGo Lite & Tavily search
│   └── scraper.py               # Async webpage scraper & text cleaner
├── graph/                       # LangGraph orchestration
│   └── research_graph.py        # StateGraph with conditional review loop
├── utils/
│   ├── llm.py                   # Unified LLM factory (Groq, OpenAI, Gemini, Anthropic)
│   └── config.py                # Environment configuration
├── frontend/                    # Modern React + Vite + Tailwind dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── AgentStatusCards.jsx
│   │   │   ├── PipelineTracker.jsx
│   │   │   ├── DebateFeed.jsx
│   │   │   ├── ReportViewer.jsx
│   │   │   ├── SettingsModal.jsx
│   │   │   └── HistoryDrawer.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── tests/                       # Unit tests
│   └── test_pipeline.py
├── server.py                    # FastAPI server with SSE streaming
├── main.py                      # Unified CLI & server launcher
├── requirements.txt             # Python dependencies
└── pyproject.toml               # Project config & linters
```

---

## 🧪 Testing

Run automated tests:
```bash
pytest tests/
```

---

## 💡 Why this is GOATed

1. **Local Logic, Cloud Compute**: Complex state machines, tool routing, and cyclical debate loops run effortlessly on your local CPU while ultra-fast cloud LLMs (like Groq LLaMA 3.3 70B) handle high-throughput GPU inference.
2. **Zero-Friction Live Search**: Built-in DuckDuckGo engine requires no paid search subscriptions.
3. **Multi-Perspective Debates**: Avoids single-model bias by forcing an internal Advocate vs. Skeptic debate before generating the report.
4. **Autonomous Peer Review**: Reviewer agent audits the output, scores factual depth, and automatically requests revisions when necessary.
