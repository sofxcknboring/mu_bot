from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timedelta
from database import Base

class Subscription(Base):
    """
    Модель подписки.
    """
    __tablename__ = "subscriptions"

    user_id = Column(Integer, primary_key=True, index=True)
    expiry_date = Column(DateTime, default=datetime.now() + timedelta(days=30))
    invite_link = Column(String, nullable=True)
    status = Column(Boolean, default=True)
