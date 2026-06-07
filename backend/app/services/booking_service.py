from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Field, TimeSlot, BookingRecord
from app.schemas import BookingCreate


def get_fields(db: Session):
    return db.query(Field).filter(Field.is_active == True).all()


def get_time_slots(db: Session):
    return db.query(TimeSlot).filter(TimeSlot.is_active == True).all()


def create_booking(db: Session, booking_data: BookingCreate):
    db_booking = BookingRecord(
        player_name=booking_data.player_name,
        phone=booking_data.phone,
        booking_date=booking_data.booking_date,
        field_id=booking_data.field_id,
        slot_id=booking_data.slot_id,
        player_count=booking_data.player_count,
        remark=booking_data.remark,
        status="confirmed"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_today_booking_count(db: Session):
    today = date.today()
    count = db.query(func.count(BookingRecord.id)).filter(
        func.date(BookingRecord.created_at) == today
    ).scalar()
    return {"count": count or 0}


def get_available_slots_for_date(db: Session, booking_date: date, field_id: int):
    slots = db.query(TimeSlot).filter(TimeSlot.is_active == True).all()
    field = db.query(Field).filter(Field.id == field_id).first()
    max_players = field.max_players if field else 20

    result = []
    for slot in slots:
        booked = db.query(func.sum(BookingRecord.player_count)).filter(
            BookingRecord.booking_date == booking_date,
            BookingRecord.field_id == field_id,
            BookingRecord.slot_id == slot.id,
            BookingRecord.status == "confirmed"
        ).scalar() or 0

        remaining = max_players - booked
        result.append({
            "id": slot.id,
            "name": slot.name,
            "start_time": slot.start_time,
            "end_time": slot.end_time,
            "max_players": max_players,
            "booked_count": booked,
            "remaining_count": remaining,
            "is_full": remaining <= 0
        })
    return result
