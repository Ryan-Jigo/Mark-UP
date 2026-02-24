from fastapi import APIRouter, HTTPException
from app.models.user import LoginRequest
from app.utils.jwt import create_access_token

router=APIRouter()

@router.post("/login")
async def login(data: LoginRequest):
    if data.email=="teacher@gmail.com" and data.password=="abcdef":
        token=create_access_token({"sub":data.email})
        return {"access_token":token,"token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")