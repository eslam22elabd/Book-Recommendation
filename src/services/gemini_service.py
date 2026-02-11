import json
from google import genai
from typing import Optional, Dict, Any
from core.config import settings

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = settings.GEMINI_MODEL

    def _generate_classification_prompt(self, query: str) -> str:
        return f"""
        You are a specialized AI assistant for a book recommendation system. 
        Analyze the query and identify the category and subcategory.
        
        # Categories and Subcategories:
        1. IT: machine_learning, deep_learning, python, data_science, artificial_intelligence
        2. Engineering: mechanical, electrical, civil, robotics, advanced_mathematics
        3. The law: criminal_law, business_law, intellectual_property, human_rights
        4. Biology: genetics, ecology, cell_biology
        5. Medicine: anatomy, pathology, clinical_neuroscience, microbiology

        Instructions:
        1. Correct potential typos or spelling errors.
        2. Assign exactly one of the categories: IT, Engineering, The law, Biology, Medicine.
        3. Assign a subcategory ONLY from those listed. If none fit perfectly, leave it empty.
        4. Return ONLY a valid JSON object. No markdown, no extra text.
        
        Query: "{query}"

        JSON Format:
        {{
            "interpreted_query": "string",
            "category": "string",
            "subcategory": "string"
        }}
        """

    def _generate_description_prompt(self, book_title: str, category: str, subcategory: str = "") -> str:
        return f"""
        Generate a concise, engaging 3-sentence book description in English for:
        Title: {book_title}
        Category: {category}
        Subcategory: {subcategory}
        Return ONLY the description text.
        """

    def classify_query(self, query: str) -> Dict[str, Any]:
        prompt = self._generate_classification_prompt(query)
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            text = response.text
            # Extract JSON
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                return json.loads(text[json_start:json_end])
        except Exception as e:
            print(f"Gemini classification error: {e}")
        return {}

    def get_book_description(self, book_title: str, category: str, subcategory: str = "") -> str:
        prompt = self._generate_description_prompt(book_title, category, subcategory)
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text.strip()
        except Exception:
            pass
        return f"A comprehensive guide to {book_title} in the field of {category}."

gemini_service = GeminiService()
