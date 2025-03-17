from typing import Optional
from fastapi import HTTPException
from notes_backend.core.supabase import supabase
from notes_backend.models.users import UserResponse, UserUpdate

class UserService:
    @staticmethod
    async def get_current_user(user_id: str) -> UserResponse:
        try:
            # Get user data from Supabase auth
            user = supabase.auth.get_user(user_id)
            
            # Get additional user data from profiles table
            profile = supabase.table("profiles").select("username").eq("id", user_id).single().execute()
            
            if not profile.data:
                raise HTTPException(status_code=404, detail="User profile not found")
            
            return UserResponse(
                email=user.user.email,
                username=profile.data["username"]
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail="User not found")

    @staticmethod
    async def update_current_user(user_id: str, user_data: UserUpdate) -> UserResponse:
        try:
            # Get user data from Supabase auth
            user = supabase.auth.get_user(user_id)
            
            # Update profile in the profiles table
            profile = supabase.table("profiles").update({
                "username": user_data.username
            }).eq("id", user_id).execute()
            
            if not profile.data:
                raise HTTPException(status_code=404, detail="User profile not found")
            
            return UserResponse(
                email=user.user.email,
                username=user_data.username
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to update user")

    @staticmethod
    async def delete_current_user(user_id: str) -> None:
        try:
            # Delete user from Supabase auth
            supabase.auth.admin.delete_user(user_id)
            
            # Profile will be automatically deleted by Supabase RLS policies
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to delete user")
