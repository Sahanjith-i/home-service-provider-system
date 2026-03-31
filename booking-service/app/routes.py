from fastapi import APIRouter, HTTPException
from app.database import collection, get_next_sequence
from app.schemas import BookingCreate, BookingResponse, BookingUpdate, MessageResponse
from app.models import booking_helper

router = APIRouter()

VALID_STATUS = ["pending", "confirmed", "completed", "cancelled"]


# CREATE BOOKING
@router.post("/bookings", response_model=BookingResponse)
def create_booking(booking: BookingCreate):
    booking_dict = booking.dict()

    booking_dict["booking_id"] = f"B{get_next_sequence('booking_id'):04d}"
    booking_dict["status"] = "pending"

    result = collection.insert_one(booking_dict)
    new_booking = collection.find_one({"_id": result.inserted_id})

    return booking_helper(new_booking)


# GET ALL BOOKINGS
@router.get("/bookings", response_model=list[BookingResponse])
def get_all_bookings():
    bookings = []
    for booking in collection.find():
        bookings.append(booking_helper(booking))
    return bookings


# GET BY booking_id
@router.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: str):
    booking = collection.find_one({"booking_id": booking_id})
    if booking:
        return booking_helper(booking)

    raise HTTPException(status_code=404, detail="Booking not found")


# UPDATE BY booking_id
@router.put("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: str, booking: BookingUpdate):
    update_data = {k: v for k, v in booking.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided")

    result = collection.update_one(
        {"booking_id": booking_id},
        {"$set": update_data}
    )

    if result.modified_count == 1:
        updated = collection.find_one({"booking_id": booking_id})
        return booking_helper(updated)

    raise HTTPException(status_code=404, detail="Booking not updated")


# DELETE BY booking_id
@router.delete("/bookings/{booking_id}", response_model=MessageResponse)
def delete_booking(booking_id: str):
    result = collection.delete_one({"booking_id": booking_id})

    if result.deleted_count == 1:
        return {"message": "Booking deleted successfully"}

    raise HTTPException(status_code=404, detail="Booking not found")


# PATCH STATUS BY booking_id
@router.patch("/bookings/{booking_id}/status", response_model=BookingResponse)
def update_status(booking_id: str, status: str):
    if status not in VALID_STATUS:
        raise HTTPException(status_code=400, detail="Invalid status value")

    result = collection.update_one(
        {"booking_id": booking_id},
        {"$set": {"status": status}}
    )

    if result.modified_count == 1:
        updated = collection.find_one({"booking_id": booking_id})
        return booking_helper(updated)

    raise HTTPException(status_code=404, detail="Status update failed")