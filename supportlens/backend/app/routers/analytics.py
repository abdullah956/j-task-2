from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models import Trace
from app.schemas import AnalyticsResponse, CategoryStat

router = APIRouter()


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(db: AsyncSession = Depends(get_db)):
    """Get analytics for all traces."""
    # Get total count
    total_count_query = select(func.count(Trace.id))
    total_result = await db.execute(total_count_query)
    total_traces = total_result.scalar() or 0

    # If no traces, return zeros
    if total_traces == 0:
        return AnalyticsResponse(
            total_traces=0,
            category_breakdown=[],
            avg_response_time_ms=0.0
        )

    # Get category breakdown
    category_query = select(
        Trace.category,
        func.count(Trace.id).label("count")
    ).group_by(Trace.category)

    category_result = await db.execute(category_query)
    category_counts = category_result.all()

    category_breakdown = [
        CategoryStat(
            category=category,
            count=count,
            percentage=round((count / total_traces) * 100, 1)
        )
        for category, count in category_counts
    ]

    # Get average response time
    avg_query = select(func.avg(Trace.response_time_ms))
    avg_result = await db.execute(avg_query)
    avg_response_time = avg_result.scalar() or 0.0

    return AnalyticsResponse(
        total_traces=total_traces,
        category_breakdown=category_breakdown,
        avg_response_time_ms=round(avg_response_time, 1)
    )
