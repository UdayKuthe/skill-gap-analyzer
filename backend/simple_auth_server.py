#!/usr/bin/env python3
"""
Simple authentication server for testing registration without database
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
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import logging
import hashlib
import secrets
from datetime import datetime, timedelta
import jwt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple models for testing
class UserRegistrationRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @field_validator('username')
    @classmethod
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
    title="Simple Skill Gap Analyzer API",
    description="Simple server for testing registration endpoint",
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

# Simple JWT token creation
def create_access_token(data: dict) -> str:
    """Create a simple JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret-key", algorithm="HS256")
    return encoded_jwt

# In-memory storage (for testing only)
users_db = {}
resumes_db = {}
analyses_db = {}

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
        
        # Check if user already exists (in-memory check)
        if user_data.email in users_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        # Create user (simulate database storage)
        user_id = len(users_db) + 1
        hashed_password = hashlib.sha256(user_data.password.encode()).hexdigest()
        
        users_db[user_data.email] = {
            "id": user_id,
            "username": user_data.username,
            "email": user_data.email,
            "password_hash": hashed_password,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Create access token
        token_data = {
            "sub": str(user_id),
            "username": user_data.username,
            "email": user_data.email
        }
        access_token = create_access_token(token_data)
        
        # Prepare response
        user_response = UserResponse(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            created_at=users_db[user_data.email]["created_at"]
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
        "message": "Simple auth server is running",
        "users_count": len(users_db)
    }

# Resumes endpoints
@app.get("/api/v1/resumes")
async def get_resumes(limit: int = 10):
    """Get user's resumes"""
    return {
        "resumes": [],
        "total": 0,
        "page": 1,
        "page_size": limit
    }

@app.post("/api/v1/resumes/upload")
async def upload_resume():
    """Upload resume endpoint"""
    return {
        "message": "Resume upload endpoint - not implemented in simple server",
        "resume_id": "test_123"
    }

# Dashboard endpoints
@app.get("/api/v1/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    return {
        "total_resumes": 0,
        "total_analyses": 0,
        "recent_analyses": 0,
        "avg_proficiency_score": None,
        "best_proficiency_score": None
    }

@app.get("/api/v1/dashboard/recent-analyses")
async def get_recent_analyses(limit: int = 5):
    """Get recent analyses"""
    return {
        "analyses": [],
        "total": 0
    }

# Analysis endpoints
@app.get("/api/v1/analysis/history")
async def get_analysis_history(limit: int = 10):
    """Get analysis history"""
    return {
        "analyses": [],
        "total_count": 0,
        "page": 1,
        "page_size": limit
    }

@app.post("/api/v1/analysis/analyze")
async def analyze_skills():
    """Analyze skills endpoint"""
    return {
        "message": "Analysis endpoint - not implemented in simple server",
        "analysis_id": "test_analysis_123"
    }

# Skills and Jobs endpoints
@app.get("/api/v1/skills-jobs/skills")
async def get_skills():
    """Get skills"""
    return {
        "skills": [],
        "total": 0
    }

@app.get("/api/v1/skills-jobs/jobs")
async def get_jobs():
    """Get jobs"""
    return {
        "jobs": [],
        "total": 0
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Simple Skill Gap Analyzer API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "register": "/api/v1/auth/register",
            "resumes": "/api/v1/resumes",
            "dashboard": "/api/v1/dashboard/stats",
            "analysis": "/api/v1/analysis/history",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting simple auth server...")
    uvicorn.run(
        "simple_auth_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
