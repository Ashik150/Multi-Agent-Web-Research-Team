"""
FastAPI Server providing real-time Server-Sent Events (SSE) streaming for the Multi-Agent Research Team.
"""
import os
import json
import asyncio
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from loguru import logger
from dotenv import load_dotenv

# Load env variables
_ROOT = Path(__file__).resolve().parent
load_dotenv(_ROOT / ".env")

from graph.research_graph import MultiAgentResearchGraph

app = FastAPI(
    title="Multi-Agent Web Research Team API",
    description="API and SSE streaming backend for autonomous multi-agent research pipelines.",
    version="1.0.0"
)

# CORS configuration for development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic: str
    provider: Optional[str] = "groq"
    model: Optional[str] = "llama-3.3-70b-versatile"
    apiKey: Optional[str] = None
    maxIterations: Optional[int] = 2


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Multi-Agent Web Research Team",
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "gemini_configured": bool(os.getenv("GOOGLE_API_KEY")),
        "anthropic_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        "tavily_configured": bool(os.getenv("TAVILY_API_KEY")),
    }


@app.get("/api/models")
async def list_models():
    """Returns available providers and recommended model configurations."""
    return {
        "providers": [
            {
                "id": "groq",
                "name": "Groq Cloud (Blistering Fast)",
                "models": [
                    {"id": "llama-3.3-70b-versatile", "name": "LLaMA 3.3 70B Versatile (Recommended)"},
                    {"id": "llama-3.1-8b-instant", "name": "LLaMA 3.1 8B Instant (Ultra Fast)"},
                    {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B (32k Context)"},
                ],
                "configured": bool(os.getenv("GROQ_API_KEY")),
                "default": True,
            },
            {
                "id": "openai",
                "name": "OpenAI",
                "models": [
                    {"id": "gpt-4o", "name": "GPT-4o (Flagship Omni)"},
                    {"id": "gpt-4o-mini", "name": "GPT-4o Mini (Fast & Smart)"},
                    {"id": "o1-mini", "name": "o1-mini (Reasoning)"},
                ],
                "configured": bool(os.getenv("OPENAI_API_KEY")),
            },
            {
                "id": "gemini",
                "name": "Google Gemini",
                "models": [
                    {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro (Massive Context)"},
                    {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash (High Speed)"},
                ],
                "configured": bool(os.getenv("GOOGLE_API_KEY")),
            },
            {
                "id": "anthropic",
                "name": "Anthropic Claude",
                "models": [
                    {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet (State-of-the-Art)"},
                    {"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku (Fast)"},
                ],
                "configured": bool(os.getenv("ANTHROPIC_API_KEY")),
            }
        ]
    }


@app.post("/api/research/stream")
async def stream_research(req: ResearchRequest):
    """
    Server-Sent Events (SSE) streaming endpoint for live research updates.
    """
    topic = req.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Research topic cannot be empty.")

    queue: asyncio.Queue = asyncio.Queue()

    async def event_callback(event: Dict[str, Any]):
        await queue.put(event)

    async def event_generator():
        # Yield initial connection confirmation
        yield f"data: {json.dumps({'agent': 'System', 'stage': 'init', 'message': f'Initializing Multi-Agent Team for: {topic}'})}\n\n"

        async def run_pipeline():
            try:
                graph = MultiAgentResearchGraph(
                    provider=req.provider,
                    model_name=req.model,
                    api_key=req.apiKey,
                )
                await graph.arun(
                    topic=topic,
                    max_iterations=req.maxIterations or 2,
                    event_callback=event_callback
                )
            except Exception as e:
                logger.error(f"Error in research pipeline: {e}")
                await queue.put({
                    "agent": "System",
                    "stage": "error",
                    "message": f"Pipeline execution error: {str(e)}"
                })
            finally:
                # Signal completion
                await queue.put(None)

        task = asyncio.create_task(run_pipeline())

        while True:
            event = await queue.get()
            if event is None:
                yield f"data: {json.dumps({'agent': 'System', 'stage': 'done', 'message': 'Research stream closed.'})}\n\n"
                break
            yield f"data: {json.dumps(event)}\n\n"

        await task

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


# Serve built frontend if static files directory exists
frontend_dist = _ROOT / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")


def start_server(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run("server:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    start_server()
