def notification_helper(notification) -> dict:
    return {
        "id": str(notification["_id"]),
        "notification_id": notification.get("notification_id"),
        "user_id": notification.get("user_id"),
        "message": notification.get("message"),
        "notification_type": notification.get("notification_type"),
        "created_at": notification.get("created_at"),
        "is_read": notification.get("is_read"),
    }