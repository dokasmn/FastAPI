# model.py
from typing import Optional
from pydantic import BaseModel

# models

class Club(BaseModel):
    id: Optional[int]
    soccer_name: str
    foundation_date: str
    amount_titles: int
    stadium: Optional[str] = None