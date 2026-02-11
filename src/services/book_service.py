import requests
from typing import List, Dict, Any, Tuple
from core.config import settings
from services.data import books_by_category, book_prices, category_keywords
from schemas.book import Book

class BookService:
    @staticmethod
    def get_book_image_url(book_title: str) -> str:
        """Fetch book cover image URL from Google Books API"""
        params = {"q": book_title, "maxResults": 1}
        try:
            response = requests.get(settings.GOOGLE_BOOKS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "items" in data and len(data["items"]) > 0:
                volume_info = data["items"][0]["volumeInfo"]
                image_links = volume_info.get("imageLinks", {})
                thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail")
                if thumbnail:
                    return thumbnail.replace("http://", "https://")
        except Exception:
            pass
        return "https://via.placeholder.com/128x195?text=No+Image"

    @staticmethod
    def get_book_price(book_title: str, category: str) -> str:
        """Get the price for a book, or return a default one if not found"""
        price = 35.99
        if category in book_prices:
            price = book_prices[category].get(book_title, book_prices[category].get('default', 35.99))
        return f"${price:.2f}"

    @classmethod
    def get_book_details(cls, book_title: str, category: str, description: str = "") -> Book:
        """Get complete book details as a Book schema"""
        return Book(
            title=book_title,
            image_url=cls.get_book_image_url(book_title),
            price=cls.get_book_price(book_title, category),
            description=description
        )

    @staticmethod
    def classify_locally(query: str) -> Tuple[str, str]:
        """Fall back to local classification if Gemini fails"""
        query_words = query.lower().split()
        
        # 1. Check for specific keywords in subcategories
        for category, subcategories in category_keywords.items():
            for subcategory, keywords in subcategories.items():
                for keyword in keywords:
                    if keyword.lower() in query.lower():
                        return category, subcategory
        
        # 2. Check for main category name match
        for category in category_keywords.keys():
            if category.lower() in query.lower().split():
                return category, ""
                
        return "Unknown", ""

    @staticmethod
    def get_books_from_inventory(category: str, subcategory: str) -> List[str]:
        """Fetch book titles from local inventory"""
        if category in books_by_category:
            if subcategory and subcategory in books_by_category[category]:
                return books_by_category[category][subcategory]
            return books_by_category[category].get('general', [])
        return []
