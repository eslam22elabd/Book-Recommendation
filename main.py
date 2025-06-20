
# Import libraries
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
from utils import classify_category, books_by_category, search_books as utils_search_books, get_book_details as utils_get_book_details

app = FastAPI()

# Query class
class Query(BaseModel):
    query: str

# Gemini API Link
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-04-17:generateContent?key=YOUR_API_KEY" 
API_KEY = "Put_your_api_here"  # Replace with your actual API key

# Function to create the improved prompt for book classification
def generate_classification_prompt(query):
    return f"""
    You are a specialized AI assistant for a book recommendation system. Your task is to understand user queries and provide relevant book recommendations. The system has the following categories and subcategories of books:

    # Categories and Subcategories:
    1. IT
       - machine_learning
       - deep_learning
       - python
       - data_science
       - artificial_intelligence
    2. Engineering
       - mechanical
       - electrical
       - civil
       - robotics
       - advanced_mathematics
    3. The law
       - criminal_law
       - business_law
       - intellectual_property
       - human_rights
    4. Biology
       - genetics 
       - ecology
       - cell_biology
    5. Medicine
       - anatomy 
       - pathology 
       - clinical_neuroscience
       - microbiology

    # Few-shot examples of understanding queries with typos or spelling errors:
    
    Example 1:
    User query: "mechnical enginiring books"
    Correct interpretation: "mechanical engineering books"
    Category: Engineering
    Subcategory: Mechanical
    
    Example 2:
    User query: "depp learning python"
    Correct interpretation: "deep learning python"
    Category: Computer Science
    Subcategory: Machine Learning
    
    Example 3: 
    User query: "artificial inteligence basics"
    Correct interpretation: "artificial intelligence basics"
    Category: Computer Science
    Subcategory: Artificial Intelligence
    
    Example 4:
    User query: "econmics theory"
    Correct interpretation: "economics theory"
    Category: Business
    Subcategory: Economics
    
    Example 5:
    User query: "netwrk security"
    Correct interpretation: "network security"
    Category: Computer Science
    Subcategory: Cybersecurity
    
    Example 6:
    User query: "electrical engineering basics"
    Correct interpretation: "electrical engineering basics"
    Category: Engineering
    Subcategory: Electrical
    
    # Instructions:
    
    1. The user might make spelling mistakes or typos in their queries.
    2. Try to understand the intent even if keywords are misspelled.
    3. Use fuzzy matching to match misspelled words with the correct categories and subcategories.
    4. Consider common typos, swapped letters, missing letters, or extra letters.
    5. If you recognize the category despite typos, provide the book recommendations for that category.
    6. Be very precise with subcategory classification - never mix different subcategories.
    7. If the query mentions "electrical", classify it as Engineering/Electrical, not as any other subcategory.
    8. Return books in JSON format with category, subcategory, and book list.
    
    # Current user query:
    "{query}"
    
    Please analyze this query, correct any potential typos or spelling errors, identify the most relevant category and subcategory, and return the appropriate book recommendations in the following JSON format:
    
    ```json
    {{
        "interpreted_query": "the corrected interpretation of the query",
        "category": "identified category",
        "subcategory": "identified subcategory (if applicable)",
        "books": [
            // list of recommended books
        ]
    }}
    ```
    """

# Function to generate a book description in English
def generate_book_description_prompt(book_title, category, subcategory=None):
    return f"""
    You are a book-description generator specialized in creating engaging and informative blurbs for readers.

    Please generate a concise but compelling description **in English** for the following book:

    • Book Title: {book_title}
    • Category: {category}
    • Subcategory: {subcategory if subcategory else 'General ' + category}

    Your description must:
    1. Be written in fluent, natural English
    2. Contain 3-5 sentences
    3. Explain what the book is about without revealing spoilers
    4. Highlight the main topics or themes covered
    5. Indicate who would benefit from reading the book

    Return **only** the description text—no extra commentary, labels, or formatting.
    """

# Function to send request to Gemini 2.5 with improved prompt
def get_books_from_api(query):
    # Create the improved prompt
    prompt = generate_classification_prompt(query)

    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.8,
            "topK": 40
        }
    }
    
    # Update the API URL to include your API key
    full_url = API_URL.replace("YOUR_API_KEY", API_KEY)
    
    response = requests.post(full_url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API request failed with status code {response.status_code}: {response.text}"}

# Function to generate description for a book
def get_book_description_from_api(book_title, category, subcategory=None):
    # Create the book description prompt
    prompt = generate_book_description_prompt(book_title, category, subcategory)

    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,  # Higher temperature for more creative descriptions
            "topP": 0.9,
            "topK": 40
        }
    }
    
    # Update the API URL to include your API key
    full_url = API_URL.replace("YOUR_API_KEY", API_KEY)
    
    try:
        response = requests.post(full_url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                description = result['candidates'][0]['content']['parts'][0]['text']
                # Clean up the description (remove extra quotes, newlines, etc.)
                description = description.strip().strip('"').strip()
                return description
            else:
                return f"Description book {book_title} In the field {category}"
        else:
            return f"Description book {book_title} In the field {category}"
    except Exception as e:
        return f"Description book {book_title} In the field {category}"

# Function to generate book image URL
def get_book_image_url(book_title, category):
    """
    Generate a URL for a book image based on its title and category.
    This is a placeholder and should be replaced with actual image URLs or API calls.
    """
    safe_title = book_title.lower().replace(' ', '-').replace(':', '').replace('\'', '')
    safe_category = category.lower().replace(' ', '-')
    return f"https://bookcovers.example.com/{safe_category}/{safe_title}.jpg"

# Enhanced function to get complete book details including price, description, and image URL
def get_complete_book_details(book_title, category, subcategory=None):
    """
    Get all book details as a dictionary including price, description, and image URL.
    """
    try:
        # Get basic book details from utils including price
        details = utils_get_book_details(book_title, category)
        
        # If utils_get_book_details returns None or an empty dict, create a new one
        if not details:
            details = {"title": book_title}
        
        # Add image URL if not already present
        if 'image_url' not in details:
            details['image_url'] = get_book_image_url(book_title, category)
        
        # Add description if not already present
        if 'description' not in details:
            details['description'] = get_book_description_from_api(book_title, category, subcategory)
        
        # Ensure price is included
        if 'price' not in details:
            # Set a default price
            details['price'] = "$29.99"  # Default price as fallback
        
        # Ensure title is included
        if 'title' not in details:
            details['title'] = book_title
        
        return details
    except Exception as e:
        # If there's any error, return a basic book object with default values
        print(f"Error getting book details for {book_title}: {str(e)}")
        return {
            "title": book_title,
            "price": "$29.99",
            "description": f"وصف كتاب {book_title} في مجال {category}",
            "image_url": get_book_image_url(book_title, category)
        }

# Endpoint to search for books
@app.post("/search-books/")
def search_books(query: Query):
    # Send the query to Gemini API
    result = get_books_from_api(query.query)
    
    # Parse the response from Gemini
    try:
        # Extract the text response from Gemini
        if 'candidates' in result and len(result['candidates']) > 0:
            response_text = result['candidates'][0]['content']['parts'][0]['text']
            
            # Find and parse the JSON response within the text
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                book_data = json.loads(response_text[json_start:json_end])
                
                # Get the interpreted category and subcategory
                category = book_data.get("category", "Unknown")
                subcategory = book_data.get("subcategory", "")
                
                print(f"Classified query '{query.query}' as Category: {category}, Subcategory: {subcategory}")
                
                # Get books from utils based on category and subcategory - be very precise here
                books_list = []
                
                # First, try to get books exactly matching the subcategory
                if subcategory and category in books_by_category:
                    if subcategory in books_by_category[category]:
                        books_list = books_by_category[category][subcategory]
                        print(f"Found {len(books_list)} books in exact category {category}/{subcategory}")
                
                # If no books found with the exact subcategory, try the general category
                if not books_list and category in books_by_category:
                    if 'general' in books_by_category[category]:
                        books_list = books_by_category[category]['general']
                        print(f"No books in exact subcategory, using {len(books_list)} books from general {category}")
                
                # Debug: If still no books found, use default subcategory-specific lists
                if not books_list:
                    print(f"No books found for {category}/{subcategory}. Using default list.")
                    
                    # Default book lists for common subcategories
                    default_books = {
                        "Electrical": [
                            "Fundamentals of Electrical Engineering",
                            "Electric Circuits",
                            "Power Electronics",
                            "Electric Machinery",
                            "Control Systems Engineering"
                        ],
                        "Mechanical": [
                            "Fundamentals of Mechanical Engineering",
                            "Thermodynamics",
                            "Fluid Mechanics",
                            "Machine Design",
                            "Engineering Materials"
                        ],
                        "Machine Learning": [
                            "Python Machine Learning",
                            "Deep Learning with Python",
                            "Hands-On Machine Learning with Scikit-Learn & TensorFlow",
                            "Pattern Recognition and Machine Learning",
                            "The Hundred-Page Machine Learning Book"
                        ],
                        "Artificial Intelligence": [
                            "Artificial Intelligence: A Modern Approach",
                            "AI Algorithms, Data Structures, and Idioms",
                            "Introduction to Artificial Intelligence",
                            "Machine Learning for AI",
                            "Neural Networks and Deep Learning"
                        ]
                    }
                    
                    # Use subcategory-specific default list if available
                    if subcategory in default_books:
                        books_list = default_books[subcategory]
                        print(f"Using default list for subcategory {subcategory}")
                    # Otherwise use a general default list
                    else:
                        books_list = [
                            f"{subcategory if subcategory else category} Fundamentals",
                            f"Introduction to {subcategory if subcategory else category}",
                            f"Advanced {subcategory if subcategory else category}",
                            f"{subcategory if subcategory else category} Handbook",
                            f"The Complete Guide to {subcategory if subcategory else category}"
                        ]
                        print(f"Using generated default list for {subcategory if subcategory else category}")
                
                # For each book, get complete details including price, description, and image URL
                recommended_books = []
                for book_title in books_list[:5]:  # Limit to 5 books
                    book_details = get_complete_book_details(book_title, category, subcategory)
                    # Debug: Print the book details to help identify any issues
                    print(f"Book details for {book_title}: {book_details}")
                    recommended_books.append(book_details)
                
                return {
                    "original_query": query.query,
                    "interpreted_query": book_data.get("interpreted_query", ""),
                    "category": category,
                    "subcategory": subcategory,
                    "recommended_books": recommended_books
                }
        
        # Fallback to local classification if Gemini response parsing fails
        raise Exception("Failed to parse Gemini response")
        
    except Exception as e:
        print(f"Exception in Gemini processing: {str(e)}")
        # Use local classification as backup
        category, subcategory = classify_category(query.query)
        
        print(f"Local classification for '{query.query}': Category: {category}, Subcategory: {subcategory}")
        
        if category == "Unknown":
            return {
                "original_query": query.query,
                "message": "Sorry, we couldn't classify your query. Please try again with a different query."
            }
        
        # Get books from utils based on category and subcategory - be very precise here
        books_list = []
        
        # First, try to get books exactly matching the subcategory
        if subcategory and category in books_by_category:
            if subcategory in books_by_category[category]:
                books_list = books_by_category[category][subcategory]
                print(f"Found {len(books_list)} books in exact category {category}/{subcategory}")
        
        # If no books found with the exact subcategory, try the general category
        if not books_list and category in books_by_category:
            if 'general' in books_by_category[category]:
                books_list = books_by_category[category]['general']
                print(f"No books in exact subcategory, using {len(books_list)} books from general {category}")
        
        # Debug: If still no books found, use default subcategory-specific lists
        if not books_list:
            print(f"No books found for {category}/{subcategory}. Using default list.")
            
            # Default book lists for common subcategories
            default_books = {
                "Electrical": [
                    "Fundamentals of Electrical Engineering",
                    "Electric Circuits",
                    "Power Electronics",
                    "Electric Machinery",
                    "Control Systems Engineering"
                ],
                "Mechanical": [
                    "Fundamentals of Mechanical Engineering",
                    "Thermodynamics",
                    "Fluid Mechanics",
                    "Machine Design",
                    "Engineering Materials"
                ],
                "Machine Learning": [
                    "Python Machine Learning",
                    "Deep Learning with Python",
                    "Hands-On Machine Learning with Scikit-Learn & TensorFlow",
                    "Pattern Recognition and Machine Learning",
                    "The Hundred-Page Machine Learning Book"
                ],
                "Artificial Intelligence": [
                    "Artificial Intelligence: A Modern Approach",
                    "AI Algorithms, Data Structures, and Idioms",
                    "Introduction to Artificial Intelligence",
                    "Machine Learning for AI",
                    "Neural Networks and Deep Learning"
                ]
            }
            
            # Use subcategory-specific default list if available
            if subcategory in default_books:
                books_list = default_books[subcategory]
                print(f"Using default list for subcategory {subcategory}")
            # Otherwise use a general default list
            else:
                books_list = [
                    f"{subcategory if subcategory else category} Fundamentals",
                    f"Introduction to {subcategory if subcategory else category}",
                    f"Advanced {subcategory if subcategory else category}",
                    f"{subcategory if subcategory else category} Handbook",
                    f"The Complete Guide to {subcategory if subcategory else category}"
                ]
                print(f"Using generated default list for {subcategory if subcategory else category}")
        
        # For each book, get complete details including price, description, and image URL
        recommended_books = []
        for book_title in books_list[:5]:  # Limit to 5 books
            book_details = get_complete_book_details(book_title, category, subcategory)
            # Debug: Print the book details to help identify any issues
            print(f"Book details for {book_title}: {book_details}")
            recommended_books.append(book_details)
        
        return {
            "original_query": query.query,
            "category": category,
            "subcategory": subcategory if subcategory else "",
            "recommended_books": recommended_books
        }

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Recommendation API"}