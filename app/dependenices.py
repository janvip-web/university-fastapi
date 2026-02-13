# from fastapi import FastAPI, status, Request, HTTPException, Depends, Response
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
# from jose import jwt, JWTError 
# from pydantic import BaseModel
# from datetime import datetime, timedelta, timezone
# from passlib.context import CryptContext
# from typing import Optional
# import bcrypt
# from app.database import get_db
# from sqlalchemy.ext.asyncio import AsyncSession


# SECRET_KEY = "8b50cea74bbf64e2f98d19426fed5ee840e734fde4d56e21525b6ad47ed61457"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# bearer_scheme = HTTPBearer()


# async def authenticate_user(db: AsyncSession, username: str, password: str):
#     user = await get_db(db, username)
#     if not user:
#         return None
#     if not pwd_context.verify(password, user.email):  # change if you store hashed pwd
#         return None
#     return user