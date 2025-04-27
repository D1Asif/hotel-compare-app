from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date, timedelta

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime = Field(alias="createdAt")

    class Config:
        from_attributes = True
        populate_by_name = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class BookmarkBase(BaseModel):
    hotel_name: str
    image: str
    price: float
    rating: float
    booking_url: str

class BookmarkCreate(BookmarkBase):
    pass

class Bookmark(BookmarkBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

    @property
    def hotelName(self) -> str:
        return self.hotel_name

    @property
    def bookingUrl(self) -> str:
        return self.booking_url

    @property
    def userId(self) -> int:
        return self.user_id

    @property
    def createdAt(self) -> datetime:
        return self.created_at

class HotelSearch(BaseModel):
    city: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    star_rating: Optional[int] = None

class LoginSchema(BaseModel):
    email: EmailStr
    password: str 