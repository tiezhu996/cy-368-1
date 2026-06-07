from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.core.database import get_db
from app.services.overview_service import get_overview
from app.services.booking_service import (
    get_fields,
    get_time_slots,
    create_booking,
    get_today_booking_count,
    get_available_slots_for_date
)
from app.schemas import (
    FieldResponse,
    TimeSlotResponse,
    BookingCreate,
    BookingResponse,
    TodayBookingStats
)

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/api/health")
def api_health():
    return {"status": "ok"}


@router.get("/overview")
def overview():
    return get_overview()


@router.get("/api/overview")
def api_overview():
    return get_overview()


@router.get("/api/fields", response_model=List[FieldResponse])
def list_fields(db: Session = Depends(get_db)):
    try:
        return get_fields(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/time-slots", response_model=List[TimeSlotResponse])
def list_time_slots(db: Session = Depends(get_db)):
    try:
        return get_time_slots(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/available-slots")
def available_slots(booking_date: date, field_id: int, db: Session = Depends(get_db)):
    try:
        return get_available_slots_for_date(db, booking_date, field_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/bookings", response_model=BookingResponse, status_code=201)
def submit_booking(booking_data: BookingCreate, db: Session = Depends(get_db)):
    try:
        if booking_data.booking_date < date.today():
            raise HTTPException(status_code=400, detail="不能预约过去的日期")

        available = get_available_slots_for_date(db, booking_data.booking_date, booking_data.field_id)
        slot_available = next((s for s in available if s["id"] == booking_data.slot_id), None)

        if not slot_available:
            raise HTTPException(status_code=400, detail="该场次不存在")

        if slot_available["is_full"]:
            raise HTTPException(status_code=400, detail="该场次已满员")

        if booking_data.player_count > slot_available["remaining_count"]:
            raise HTTPException(
                status_code=400,
                detail=f"预约人数超过剩余名额，当前剩余 {slot_available['remaining_count']} 人"
            )

        booking = create_booking(db, booking_data)
        return BookingResponse(
            id=booking.id,
            player_name=booking.player_name,
            phone=booking.phone,
            booking_date=booking.booking_date,
            field_id=booking.field_id,
            field_name=booking.field.name if booking.field else None,
            slot_id=booking.slot_id,
            slot_name=booking.slot.name if booking.slot else None,
            player_count=booking.player_count,
            status=booking.status,
            remark=booking.remark,
            created_at=booking.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/bookings/today/count", response_model=TodayBookingStats)
def today_booking_count(db: Session = Depends(get_db)):
    try:
        return get_today_booking_count(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
