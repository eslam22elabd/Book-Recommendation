from fastapi import APIRouter, HTTPException
from schemas.book import Query, BookResponse, Book
from services.gemini_service import gemini_service
from services.book_service import BookService
from services.data import default_fallback_books

router = APIRouter()

@router.post("/search-books/", response_model=BookResponse)
def search_books(query: Query):
    # 1. Try AI classification
    ai_result = gemini_service.classify_query(query.query)
    
    category = ai_result.get("category", "Unknown")
    subcategory = ai_result.get("subcategory", "")
    interpreted_query = ai_result.get("interpreted_query", query.query)
    
    # 2. Fallback to local classification if AI failed
    if category == "Unknown":
        category, subcategory = BookService.classify_locally(query.query)
        
    if category == "Unknown":
        return BookResponse(
            original_query=query.query,
            category="Unknown",
            recommended_books=[],
            message="Sorry, we couldn't classify your query. Please try again."
        )

    # 3. Get books from inventory
    book_titles = BookService.get_books_from_inventory(category, subcategory)
    
    # 4. Fallback to default lists if inventory is empty
    if not book_titles:
        book_titles = default_fallback_books.get(subcategory, [
            f"Introduction to {subcategory or category}",
            f"Advanced {subcategory or category}"
        ])

    # 5. Build rich book details
    recommended_books = []
    for title in book_titles[:5]:
        description = gemini_service.get_book_description(title, category, subcategory)
        book_details = BookService.get_book_details(title, category, description)
        recommended_books.append(book_details)

    return BookResponse(
        original_query=query.query,
        interpreted_query=interpreted_query,
        category=category,
        subcategory=subcategory,
        recommended_books=recommended_books
    )
