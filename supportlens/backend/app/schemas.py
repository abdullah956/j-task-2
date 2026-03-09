from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List

from app.models import CategoryEnum


class TraceCreate(BaseModel):
    user_message: str
    bot_response: str
    response_time_ms: int


class TraceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_message: str
    bot_response: str
    category: CategoryEnum
    timestamp: datetime
    response_time_ms: int


class CategoryStat(BaseModel):
    category: CategoryEnum
    count: int
    percentage: float


class AnalyticsResponse(BaseModel):
    total_traces: int
    category_breakdown: List[CategoryStat]
    avg_response_time_ms: float


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    response_time_ms: int
