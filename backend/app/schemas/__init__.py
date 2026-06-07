from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional


class FieldResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    max_players: int

    class Config:
        from_attributes = True


class TimeSlotResponse(BaseModel):
    id: int
    name: str
    start_time: time
    end_time: time

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    player_name: str = Field(..., min_length=1, max_length=80)
    phone: str = Field(..., min_length=7, max_length=20)
    booking_date: date
    field_id: int
    slot_id: int
    player_count: int = Field(..., ge=1, le=30)
    remark: Optional[str] = Field(None, max_length=255)


class BookingResponse(BaseModel):
    id: int
    player_name: str
    phone: str
    booking_date: date
    field_id: int
    field_name: Optional[str]
    slot_id: int
    slot_name: Optional[str]
    player_count: int
    status: str
    remark: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class TodayBookingStats(BaseModel):
    count: int
