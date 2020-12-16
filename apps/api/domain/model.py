from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    publisher: str
    pages: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Tag(BaseModel):
    id: int
    name: str