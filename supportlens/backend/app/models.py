import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class CategoryEnum(str, enum.Enum):
    BILLING = "Billing"
    REFUND = "Refund"
    ACCOUNT_ACCESS = "Account Access"
    CANCELLATION = "Cancellation"
    GENERAL_INQUIRY = "General Inquiry"


class Trace(Base):
    __tablename__ = "traces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    response_time_ms = Column(Integer, nullable=False)
