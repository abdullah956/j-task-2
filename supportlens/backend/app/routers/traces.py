from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from typing import Optional, List

from app.database import get_db
from app.models import Trace, CategoryEnum
from app.schemas import TraceCreate, TraceResponse, ChatRequest, ChatResponse
from app.services.classifier import classify_trace
from app.services.llm import GroqClient, CHATBOT_SYSTEM_PROMPT

router = APIRouter()


@router.post("/traces", response_model=TraceResponse)
async def create_trace(
    trace_data: TraceCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new trace by classifying it and saving to the database."""
    # Classify the trace
    category_str = await classify_trace(
        user_message=trace_data.user_message,
        bot_response=trace_data.bot_response
    )

    # Convert string to enum
    category_enum = CategoryEnum(category_str)

    # Create trace object
    trace = Trace(
        user_message=trace_data.user_message,
        bot_response=trace_data.bot_response,
        category=category_enum,
        response_time_ms=trace_data.response_time_ms
    )

    # Save to database
    db.add(trace)
    await db.commit()
    await db.refresh(trace)

    return trace


@router.get("/traces", response_model=List[TraceResponse])
async def get_traces(
    category: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get all traces, optionally filtered by category."""
    query = select(Trace).order_by(Trace.timestamp.desc())

    # Apply category filter if provided
    if category:
        category_enum = CategoryEnum(category)
        query = query.where(Trace.category == category_enum)

    result = await db.execute(query)
    traces = result.scalars().all()

    return traces


@router.get("/traces/search", response_model=List[TraceResponse])
async def search_traces(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    """Search traces by user message or bot response (case-insensitive)."""
    search_term = f"%{q}%"

    query = select(Trace).where(
        or_(
            func.lower(Trace.user_message).like(func.lower(search_term)),
            func.lower(Trace.bot_response).like(func.lower(search_term))
        )
    ).order_by(Trace.timestamp.desc())

    result = await db.execute(query)
    traces = result.scalars().all()

    return traces


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the support bot without saving to database."""
    groq_client = GroqClient()

    response_text, response_time_ms = await groq_client.chat_complete(
        system_prompt=CHATBOT_SYSTEM_PROMPT,
        user_message=request.message
    )

    return ChatResponse(
        response=response_text,
        response_time_ms=response_time_ms
    )
