from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    description = Column(String(255))
    max_players = Column(Integer, nullable=False, default=20)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    bookings = relationship("BookingRecord", back_populates="field")


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    bookings = relationship("BookingRecord", back_populates="slot")


class BookingRecord(Base):
    __tablename__ = "booking_records"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String(80), nullable=False)
    phone = Column(String(20), nullable=False)
    booking_date = Column(Date, nullable=False, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("time_slots.id"), nullable=False)
    player_count = Column(Integer, nullable=False, default=1)
    status = Column(String(20), default="pending", index=True)
    remark = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    field = relationship("Field", back_populates="bookings")
    slot = relationship("TimeSlot", back_populates="bookings")
