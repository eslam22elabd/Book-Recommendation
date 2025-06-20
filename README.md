## Book Recommendation API
This API provides book recommendations based on user queries, categorized across various domains such as IT, Engineering, Law, Biology, and Medicine. The API uses FastAPI and integrates with Google Books API to retrieve relevant book data, including titles, prices, descriptions, and images. Additionally, the API offers fuzzy matching for typos and spelling errors in user input, ensuring accurate book classification and recommendations.

## Features
Book Categories: IT, Engineering, Law, Biology, Medicine.

Subcategory Classification: Each category has specific subcategories for a more refined recommendation system.

Price Information: Each book has a default price, with exceptions for specific titles.

Image URLs: Fetch book cover images from the Google Books API.

Fuzzy Matching: Handles misspelled queries and suggests books accordingly.

Recommendation Generation: Provides books based on the input query and the classified category.

## Technologies Used
FastAPI: For creating the web framework to handle API requests.

Google Books API: For retrieving book details like image URLs.

Pydantic: For data validation using BaseModel to structure the queries.

Python: General-purpose programming language to write the backend logic.

Requests: For making HTTP requests to the Google Books API.

# Installation
pip install -r requirements.txt

# Usage
Run the FastAPI server: uvicorn main:app --reload

## Customization
Books Data: The books_by_category dictionary can be modified to include more books or categories.

Google Books API: Modify the get_book_image_url function to change how the book images are fetched.

API Key: Ensure that your Google API key is set in the API_KEY variable in main.py.

## Acknowledgements
FastAPI
Google Books API