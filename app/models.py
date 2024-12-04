from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WeatherCreate(BaseModel):
    city: str = Field(..., min_length=2, max_length=100, description="Название города")

class WeatherResponse(BaseModel):
    id: Optional[int] 
    city: str
    temperature: float
    description: str
    timestamp: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None