def booking_helper(booking) -> dict:
    return {
        "id": str(booking["_id"]),
        "booking_id": booking.get("booking_id"),
        "customer_id": booking.get("customer_id"),
        "provider_id": booking.get("provider_id"),
        "service_type": booking.get("service_type"),
        "booking_date": booking.get("booking_date"),
        "address": booking.get("address"),
        "status": booking.get("status"),
    }