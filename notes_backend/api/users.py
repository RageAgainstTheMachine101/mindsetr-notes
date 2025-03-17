from fastapi import APIRouter, Depends, HTTPException
from notes_backend.core.supabase import supabase
from notes_backend.models.users import UserResponse, UserUpdate
from notes_backend.services.users import UserService
from notes_backend.core.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["users"])

@router.get("/current", response_model=UserResponse)
async def get_current_user_profile(user_id: str = Depends(get_current_user)):
    """Get current user profile"""
    return await UserService.get_current_user(user_id)

@router.put("/current", response_model=UserResponse)
async def update_current_user_profile(
    user_data: UserUpdate,
    user_id: str = Depends(get_current_user)
):
    """Update current user profile"""
    return await UserService.update_current_user(user_id, user_data)

@router.delete("/current")
async def delete_current_user_profile(user_id: str = Depends(get_current_user)):
    """Delete current user profile"""
    await UserService.delete_current_user(user_id)
    return {"message": "User deleted successfully"}
