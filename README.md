# 📚 Book Recommendation API

A professional, modular, and AI-powered book recommendation engine built with **FastAPI** and **Google Gemini SDK**.

## 🌟 Features

- **MVC Architecture**: Clean separation of concerns in the `src/` directory.
- **Official SDK**: Uses `google-generativeai` for high-performance AI interactions.
- **AI-Powered Search**: Uses **Gemini 1.5 Flash** for intelligent query classification.
- **Rich Book Data**: Integrates with **Google Books API** for real-time book covers.
- **Dynamic Descriptions**: Generates unique, engaging blurbs for every recommendation.
- **Secure Configuration**: Environment-based configuration management using `pydantic-settings`.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI SDK**: [Google Generative AI](https://pypi.org/project/google-generativeai/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- A Google AI (Gemini) API Key

### 2. Installation
```bash
# Clone the repository
git clone <repo-url>
cd Book-Recommendation

# Install dependencies
pip install -r src/requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
API_KEY=your_gemini_api_key_here
```

### 4. Running the API
```bash
python -m uvicorn src.main:app --reload
```
The API will be available at `http://localhost:8000`.

## 📖 API Documentation

- **Interactive Swagger UI**: `http://localhost:8000/docs`

### Example Request
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/search-books/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "machine learning with python"
}'
```

## 📁 Project Structure

```text
├── src/
│   ├── api/          # Route handlers (Controllers)
│   ├── core/         # Config and settings
│   ├── schemas/      # Pydantic models
│   ├── services/     # Business logic & AI interactions
│   ├── main.py       # App entry point
│   └── requirements.txt
├── .env              # Environment variables
└── README.md
```
