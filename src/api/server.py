"""FastAPI Server - Main API and CLI test interface"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="ProjectXI LLM",
    description="Groq Agent MVP for content generation and QA",
    version="0.1.0"
)


class QueryRequest(BaseModel):
    """Request model for queries"""
    query: str
    context: str = ""


class QueryResponse(BaseModel):
    """Response model for queries"""
    answer: str
    model: str
    tokens_used: int = 0


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a query using the Groq agent.

    Args:
        request: Query request with question and optional context

    Returns:
        Query response with answer and metadata
    """
    # TODO: Implement agent processing
    return QueryResponse(
        answer="Implementation pending",
        model="groq-agent",
        tokens_used=0
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ProjectXI LLM API FUNCIONAAAAAAA",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
