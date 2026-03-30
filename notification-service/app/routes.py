from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
from app.database import collection, get_next_sequence
from app.schemas import NotificationCreate
from app.models import notification_helper

router = APIRouter()


# 🔹 CREATE NOTIFICATION
@router.post("/notifications")
def create_notification(notification: NotificationCreate):
    notification_dict = notification.model_dump()

    # If still using `type`, normalize it to `notification_type`
    if "type" in notification_dict and "notification_type" not in notification_dict:
        notification_dict["notification_type"] = notification_dict["type"]

    # remove temporary field `type` before insertion
    notification_dict.pop("type", None)

    # 🔥 AUTO INCREMENT ID
    notification_dict["notification_id"] = f"N{get_next_sequence('notification_id'):04d}"

    result = collection.insert_one(notification_dict)
    new_notification = collection.find_one({"_id": result.inserted_id})

    return notification_helper(new_notification)


# 🔹 GET ALL
@router.get("/notifications")
def get_notifications():
    notifications = []
    for notification in collection.find():
        notifications.append(notification_helper(notification))
    return notifications


# 🔹 GET BY notification_id
@router.get("/notifications/{notification_id}")
def get_notification(notification_id: str):
    notification = collection.find_one({"notification_id": notification_id})

    if notification:
        return notification_helper(notification)

    raise HTTPException(status_code=404, detail="Notification not found")


# 🔹 UPDATE
@router.put("/notifications/{notification_id}")
def update_notification(notification_id: str, notification: NotificationCreate):
    update_data = notification.model_dump()

    result = collection.update_one(
        {"notification_id": notification_id},
        {"$set": update_data}
    )

    if result.modified_count == 1:
        updated = collection.find_one({"notification_id": notification_id})
        return notification_helper(updated)

    raise HTTPException(status_code=404, detail="Notification not updated")


# 🔹 DELETE
@router.delete("/notifications/{notification_id}")
def delete_notification(notification_id: str):
    result = collection.delete_one({"notification_id": notification_id})

    if result.deleted_count == 1:
        return {"message": "Notification deleted successfully"}

    raise HTTPException(status_code=404, detail="Notification not found")


# 🔹 PATCH → mark as read
@router.patch("/notifications/{notification_id}/read")
def mark_as_read(notification_id: str):
    result = collection.update_one(
        {"notification_id": notification_id},
        {"$set": {"is_read": True}}
    )

    if result.modified_count == 1:
        updated = collection.find_one({"notification_id": notification_id})
        return notification_helper(updated)

    raise HTTPException(status_code=404, detail="Update failed")