from pydantic import BaseModel
from typing import List, Optional

class Query(BaseModel):
    query: str

class Book(BaseModel):
    title: str
    price: str
    description: str
    image_url: str

class BookResponse(BaseModel):
    original_query: str
    interpreted_query: Optional[str] = None
    category: str
    subcategory: Optional[str] = ""
    recommended_books: List[Book]
    message: Optional[str] = None
