from fastapi import APIRouter, HTTPException, status
from bson.objectid import ObjectId
from datetime import datetime
from passlib.context import CryptContext
import re

from .database import get_customers_collection, create_customer_id, convert_object_id
from .schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    UpdateProfileRequest,
    CustomerDetailResponse,
    AllCustomersResponse,
)

router = APIRouter(prefix="/customers", tags=["customers"])

# Password hashing using argon2 (no byte limit, more secure than bcrypt)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using argon2 (no 72-byte limit, more secure)"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number (basic validation)"""
    phone = phone.replace(" ", "").replace("-", "").replace("+", "")
    return phone.isdigit() and len(phone) >= 10


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_customer(request: RegisterRequest):
    """Register a new customer"""
    customers = get_customers_collection()

    # Validate email format
    if not validate_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate phone format
    if not validate_phone(request.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number format"
        )

    # Check if email already exists
    existing_customer = customers.find_one({"email": request.email.lower()})
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new customer
    customer_id = create_customer_id()
    now = datetime.utcnow()

    customer_data = {
        "customer_id": customer_id,
        "name": request.name,
        "email": request.email.lower(),
        "phone": request.phone,
        "address": request.address,
        "city": request.city,
        "state": request.state,
        "postal_code": request.postal_code,
        "password_hash": hash_password(request.password),
        "created_at": now,
        "updated_at": now,
    }

    result = customers.insert_one(customer_data)

    if result.inserted_id:
        return RegisterResponse(
            success=True,
            message="Customer registered successfully",
            customer_id=customer_id
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register customer"
        )


@router.post("/login", response_model=LoginResponse)
async def login_customer(request: LoginRequest):
    """Login a customer"""
    customers = get_customers_collection()

    # Find customer by email
    customer = customers.find_one({"email": request.email.lower()})

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, customer["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Prepare customer data (without password hash)
    customer_data = {
        "customer_id": customer["customer_id"],
        "name": customer["name"],
        "email": customer["email"],
        "phone": customer["phone"],
        "address": customer["address"],
        "city": customer.get("city"),
        "state": customer.get("state"),
        "postal_code": customer.get("postal_code"),
        "created_at": str(customer["created_at"]),
        "updated_at": str(customer["updated_at"]),
    }

    return LoginResponse(
        success=True,
        message="Login successful",
        customer=customer_data,
        token=customer["customer_id"]  # Use customer_id as token (in production, use JWT)
    )


@router.get("", response_model=AllCustomersResponse)
async def get_all_customers(skip: int = 0, limit: int = 10):
    """Get all customers with pagination"""
    customers = get_customers_collection()

    # Validate pagination parameters
    if skip < 0 or limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pagination parameters"
        )

    # Get total count
    total = customers.count_documents({})

    # Get customers with pagination
    customer_list = list(
        customers.find({})
        .skip(skip)
        .limit(limit)
        .sort("created_at", -1)
    )

    # Convert to response format
    customers_data = []
    for customer in customer_list:
        customers_data.append(CustomerDetailResponse(
            customer_id=customer["customer_id"],
            name=customer["name"],
            email=customer["email"],
            phone=customer["phone"],
            address=customer["address"],
            city=customer.get("city"),
            state=customer.get("state"),
            postal_code=customer.get("postal_code"),
            created_at=customer["created_at"].isoformat(),
            updated_at=customer["updated_at"].isoformat(),
        ))

    return AllCustomersResponse(total=total, customers=customers_data)


@router.get("/{customer_id}", response_model=CustomerDetailResponse)
async def get_customer_by_id(customer_id: str):
    """Get customer by customer_id"""
    customers = get_customers_collection()

    customer = customers.find_one({"customer_id": customer_id})

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return CustomerDetailResponse(
        customer_id=customer["customer_id"],
        name=customer["name"],
        email=customer["email"],
        phone=customer["phone"],
        address=customer["address"],
        city=customer.get("city"),
        state=customer.get("state"),
        postal_code=customer.get("postal_code"),
        created_at=customer["created_at"].isoformat(),
        updated_at=customer["updated_at"].isoformat(),
    )


@router.put("/{customer_id}", response_model=CustomerDetailResponse)
async def update_customer(customer_id: str, request: UpdateProfileRequest):
    """Update customer profile"""
    customers = get_customers_collection()

    # Find customer
    customer = customers.find_one({"customer_id": customer_id})
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # Prepare update data
    update_data = {}
    
    if request.name is not None:
        if len(request.name) < 1 or len(request.name) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name must be between 1 and 100 characters"
            )
        update_data["name"] = request.name

    if request.phone is not None:
        if not validate_phone(request.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number format"
            )
        update_data["phone"] = request.phone

    if request.address is not None:
        if len(request.address) < 5 or len(request.address) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address must be between 5 and 500 characters"
            )
        update_data["address"] = request.address

    if request.city is not None:
        update_data["city"] = request.city

    if request.state is not None:
        update_data["state"] = request.state

    if request.postal_code is not None:
        update_data["postal_code"] = request.postal_code

    # Always update the updated_at timestamp
    update_data["updated_at"] = datetime.utcnow()

    # Update customer
    result = customers.find_one_and_update(
        {"customer_id": customer_id},
        {"$set": update_data},
        return_document=True
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update customer"
        )

    return CustomerDetailResponse(
        customer_id=result["customer_id"],
        name=result["name"],
        email=result["email"],
        phone=result["phone"],
        address=result["address"],
        city=result.get("city"),
        state=result.get("state"),
        postal_code=result.get("postal_code"),
        created_at=result["created_at"].isoformat(),
        updated_at=result["updated_at"].isoformat(),
    )


@router.patch("/{customer_id}", response_model=CustomerDetailResponse)
async def patch_customer(customer_id: str, request: UpdateProfileRequest):
    """Partially update customer profile (PATCH)"""
    customers = get_customers_collection()

    # Find customer
    customer = customers.find_one({"customer_id": customer_id})
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # Prepare update data (only update provided fields)
    update_data = {}
    
    if request.name is not None:
        if len(request.name) < 1 or len(request.name) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name must be between 1 and 100 characters"
            )
        update_data["name"] = request.name

    if request.phone is not None:
        if not validate_phone(request.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number format"
            )
        update_data["phone"] = request.phone

    if request.address is not None:
        if len(request.address) < 5 or len(request.address) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address must be between 5 and 500 characters"
            )
        update_data["address"] = request.address

    if request.city is not None:
        update_data["city"] = request.city

    if request.state is not None:
        update_data["state"] = request.state

    if request.postal_code is not None:
        update_data["postal_code"] = request.postal_code

    # If no fields to update, return current customer
    if not update_data:
        return CustomerDetailResponse(
            customer_id=customer["customer_id"],
            name=customer["name"],
            email=customer["email"],
            phone=customer["phone"],
            address=customer["address"],
            city=customer.get("city"),
            state=customer.get("state"),
            postal_code=customer.get("postal_code"),
            created_at=customer["created_at"].isoformat(),
            updated_at=customer["updated_at"].isoformat(),
        )

    # Always update the updated_at timestamp when changes are made
    update_data["updated_at"] = datetime.utcnow()

    # Update customer
    result = customers.find_one_and_update(
        {"customer_id": customer_id},
        {"$set": update_data},
        return_document=True
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update customer"
        )

    return CustomerDetailResponse(
        customer_id=result["customer_id"],
        name=result["name"],
        email=result["email"],
        phone=result["phone"],
        address=result["address"],
        city=result.get("city"),
        state=result.get("state"),
        postal_code=result.get("postal_code"),
        created_at=result["created_at"].isoformat(),
        updated_at=result["updated_at"].isoformat(),
    )


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: str):
    """Delete a customer"""
    customers = get_customers_collection()

    # Find and delete customer
    result = customers.delete_one({"customer_id": customer_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return None
