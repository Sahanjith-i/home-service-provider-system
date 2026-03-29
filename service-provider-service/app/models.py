def provider_serializer(provider) -> dict:
    return {
        "provider_id": provider.get("provider_id"),
        "name": provider.get("name"),
        "service_type": provider.get("service_type"),
        "phone": provider.get("phone"),
        "email": provider.get("email"),
        "location": provider.get("location"),
        "availability_status": provider.get("availability_status"),
    }


def providers_serializer(providers) -> list:
    return [provider_serializer(provider) for provider in providers]