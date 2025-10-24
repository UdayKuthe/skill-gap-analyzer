#!/usr/bin/env python3
"""
Simple test server to test the registration endpoint without database dependencies
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
backend_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_root))

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple models for testing
class UserRegistrationRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('username')
    def username_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Username cannot be empty')
        return v.strip()

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

# Create FastAPI app
app = FastAPI(
    title="Test Skill Gap Analyzer API",
    description="Test server for registration endpoint",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Simple password validation
def validate_password(password: str) -> dict:
    """Validate password strength"""
    if len(password) < 8:
        return {"valid": False, "message": "Password must be at least 8 characters long"}
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not has_upper:
        return {"valid": False, "message": "Password must contain at least one uppercase letter"}
    
    if not has_lower:
        return {"valid": False, "message": "Password must contain at least one lowercase letter"}
    
    if not has_digit:
        return {"valid": False, "message": "Password must contain at least one number"}
    
    return {"valid": True, "message": "Password is strong"}

# Simple email validation
def validate_email(email: str) -> bool:
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Registration endpoint
@app.post("/api/v1/auth/register", 
         response_model=TokenResponse,
         status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegistrationRequest):
    """
    Register a new user (test endpoint without database)
    """
    try:
        # Validate email format
        if not validate_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Validate password strength
        password_validation = validate_password(user_data.password)
        if not password_validation["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=password_validation["message"]
            )
        
        # Simulate user creation (without database)
        user_id = 1  # Simulated user ID
        access_token = "test_token_12345"  # Simulated token
        
        # Prepare response
        user_response = UserResponse(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            created_at="2024-01-01T00:00:00Z"
        )
        
        logger.info(f"User registered successfully: {user_data.email}")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=3600,
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Test server is running"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Test Skill Gap Analyzer API",
        "version": "1.0.0",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting test server...")
    uvicorn.run(
        "test_server:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
