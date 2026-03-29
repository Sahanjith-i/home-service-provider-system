from fastapi import APIRouter, HTTPException
from app.database import provider_collection, get_next_provider_id
from app.schemas import ServiceProviderCreate, ServiceProviderUpdate
from app.models import provider_serializer, providers_serializer

router = APIRouter()


@router.post("/providers")
def create_provider(provider: ServiceProviderCreate):
    provider_dict = provider.dict()
    provider_dict["provider_id"] = get_next_provider_id()

    result = provider_collection.insert_one(provider_dict)
    new_provider = provider_collection.find_one({"_id": result.inserted_id})

    return {
        "message": "Service provider created successfully",
        "provider": provider_serializer(new_provider)
    }


@router.get("/providers")
def get_all_providers():
    providers = provider_collection.find().sort("provider_id", 1)
    return providers_serializer(providers)


@router.get("/providers/{provider_id}")
def get_provider_by_id(provider_id: int):
    provider = provider_collection.find_one({"provider_id": provider_id})

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider_serializer(provider)


@router.put("/providers/{provider_id}")
def update_provider(provider_id: int, provider: ServiceProviderUpdate):
    existing_provider = provider_collection.find_one({"provider_id": provider_id})
    if not existing_provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    update_data = {k: v for k, v in provider.dict().items() if v is not None}

    if update_data:
        provider_collection.update_one(
            {"provider_id": provider_id},
            {"$set": update_data}
        )

    updated_provider = provider_collection.find_one({"provider_id": provider_id})

    return {
        "message": "Service provider updated successfully",
        "provider": provider_serializer(updated_provider)
    }


@router.patch("/providers/{provider_id}/phone")
def update_provider_phone(provider_id: int, phone: str):
    existing_provider = provider_collection.find_one({"provider_id": provider_id})
    if not existing_provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    provider_collection.update_one(
        {"provider_id": provider_id},
        {"$set": {"phone": phone}}
    )

    updated_provider = provider_collection.find_one({"provider_id": provider_id})

    return {
        "message": "Phone number updated successfully",
        "provider": provider_serializer(updated_provider)
    }


@router.delete("/providers/{provider_id}")
def delete_provider(provider_id: int):
    existing_provider = provider_collection.find_one({"provider_id": provider_id})
    if not existing_provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    provider_collection.delete_one({"provider_id": provider_id})

    return {"message": "Service provider deleted successfully"}