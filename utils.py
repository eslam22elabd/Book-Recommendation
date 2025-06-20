
import requests
# List of books for each category with detailed subcategories
books_by_category = {
    'IT': {
        'general': [
            'Python for Beginners', 
            'Data Science with Python', 
            'Hands-On Machine Learning with Scikit-Learn', 
            'Deep Learning with Python', 
            'Machine Learning Yearning', 
            'Artificial Intelligence: A Modern Approach', 
            'Learning Python', 
            'Practical Statistics for Data Scientists', 
            'Introduction to Algorithms', 
            'Data Science from Scratch', 
            'Programming Collective Intelligence', 
            'Automate the Boring Stuff with Python', 
            'The Pragmatic Programmer', 
            'Fluent Python', 
            'Introduction to Machine Learning with Python'
        ],
        'machine_learning': [
            'Hands-On Machine Learning with Scikit-Learn',
            'Deep Learning with Python',
            'Machine Learning Yearning',
            'Introduction to Machine Learning with Python'
        ],
        'deep_learning': [
            'Deep Learning with Python',
            'Hands-On Machine Learning with Scikit-Learn',
        ],
        'python': [
            'Python for Beginners',
            'Learning Python',
            'Fluent Python',
            'Automate the Boring Stuff with Python'
        ],
        'data_science': [
            'Data Science with Python',
            'Data Science from Scratch',
            'Practical Statistics for Data Scientists'
        ],
        'artificial_intelligence': [
            'Artificial Intelligence: A Modern Approach',
            'Machine Learning Yearning',
            'Artificial Intelligence: A Guide for Thinking Humans'
        ]
    },
    
    'Engineering': {
        'general': [
            'Introduction to Mechanical Engineering',
            'Engineering Mechanics: Dynamics',
            'Advanced Engineering Mathematics',
            'Engineering Materials 1',
            'Electric Power Systems',
            'Introduction to Robotics',
            'Statics and Mechanics of Materials',
            'The Art of Electronics',
            'Fundamentals of Heat and Mass Transfer',
            'Building Construction Illustrated'
        ],
        'mechanical': [
            'Introduction to Mechanical Engineering',
            'Mechanical Engineering Design',
            'Fluid Mechanics',
            'Introduction to Structural Engineering',
            'Heat Transfer'
        ],
        'electrical': [
            'Electrical Engineering Fundamentals',
            'Electric Power Systems',
            'Introduction to Robotics',
            'Circuit Analysis'
        ],
        'civil': [
            'Civil Engineering: A Very Short Introduction',
            'Introduction to Structural Engineering',
            'Building Construction Illustrated',
            'Structural Analysis'
        ],
        'robotics': [
            'Introduction to Robotics',
            'Robotics: Control, Sensing, Vision, and Intelligence',
            'Robotics: Modelling, Planning, and Control'
        ],
        'advanced_mathematics': [
            'Advanced Engineering Mathematics',
            'Mathematics for Engineers',
            'Applied Mathematics for Engineers'
        ]
    },

    'The law': {
        'general': [
            'The Law of Contracts',
            'Introduction to Constitutional Law',
            'International Human Rights Law',
            'Criminal Law Handbook',
            'Civil Procedure',
            'Family Law and Practice',
            'Business Law for Entrepreneurs',
            'Legal Aspects of Business',
            'Torts',
            'Principles of Contract Law',
            'The Legal Environment of Business',
            'Intellectual Property Law',
            'Law and Ethics in the Business World',
            'Understanding Constitutional Law',
            'Law and Society'
        ],
        'criminal_law': [
            'Criminal Law Handbook',
            'International Human Rights Law',
            'The Law of Contracts'
        ],
        'business_law': [
            'Business Law for Entrepreneurs',
            'Legal Aspects of Business',
            'Principles of Contract Law'
        ],
        'intellectual_property': [
            'Intellectual Property Law',
            'Patent Law',
            'Copyright Law'
        ],
        'human_rights': [
            'International Human Rights Law',
            'The Law of Human Rights'
        ]
    },

    'Biology': {
        'general': [
            'Biology: The Essentials',
            'Molecular Biology of the Cell',
            'Human Anatomy and Physiology',
            'Ecology: Concepts and Applications',
            'Biology: A Global Approach',
            'The Selfish Gene',
            'The Origin of Species',
            'The Structure of Evolutionary Theory',
            'Principles of Biology',
            'Introduction to Cell Biology',
            'The Biology of Cancer',
            'Genetics: A Conceptual Approach',
            'Plant Biology Essentials',
            'Biochemistry',
            'The Diversity of Life'
        ],
        'genetics': [
            'Genetics: A Conceptual Approach',
            'The Selfish Gene',
            'The Origin of Species',
            'Molecular Biology of the Cell'
        ],
        'ecology': [
            'Ecology: Concepts and Applications',
            'The Diversity of Life',
            'Biology: A Global Approach',
            'Ecology: From Individuals to Ecosystems'
        ],
        'cell_biology': [
            'Introduction to Cell Biology',
            'Molecular Biology of the Cell',
            'The Biology of Cancer'
        ]
    },

    'Medicine': {
        'general': [
            'The Human Body in Health and Disease',
            'The Merck Manual of Diagnosis and Therapy',
            'Medical Physiology',
            'Pathophysiology of Disease',
            'Basic Clinical Neuroscience',
            'Medical Microbiology',
            'Anatomy & Physiology for Health Professions',
            'Medical Terminology: A Living Language',
            'Pathology: The Big Picture',
            'Principles of Internal Medicine',
            'Robbins and Cotran Pathologic Basis of Disease',
            'Harrison\'s Principles of Internal Medicine',
            'Essentials of Family Medicine',
            'Clinical Examination: A Systematic Guide to Physical Diagnosis',
            'Diagnostic and Statistical Manual of Mental Disorders'
        ],
        'anatomy': [
            'The Human Body in Health and Disease',
            'Anatomy & Physiology for Health Professions',
            'Clinical Examination: A Systematic Guide to Physical Diagnosis'
        ],
        'pathology': [
            'Pathology: The Big Picture',
            'Robbins and Cotran Pathologic Basis of Disease',
            'Diagnostic and Statistical Manual of Mental Disorders'
        ],
        'clinical_neuroscience': [
            'Basic Clinical Neuroscience',
            'Clinical Neuroanatomy',
            'Neurology: A Queen Square Textbook'
        ],
        'microbiology': [
            'Medical Microbiology',
            'Microbiology: A Human Perspective',
            'Clinical Microbiology Made Ridiculously Simple'
        ]
    }
}

# Keywords with precise subcategories
category_keywords = {
    'IT': {
        'machine_learning': ['machine learning', 'deep learning', 'neural networks', 'تعلم الآلة', 'ذكاء اصطناعي'],
        'python': ['python', 'برمجة بايثون', 'Learning Python', 'Fluent Python'],
        'deep_learning': ['deep learning', 'neural networks', 'شبكات عصبية'],
        'data_science': ['data science', 'علم البيانات', 'تحليل البيانات'],
        'artificial_intelligence': ['artificial intelligence', 'AI', 'ذكاء اصطناعي']
    },
    'Engineering': {
        'mechanical': ['mechanical', 'fluid mechanics', 'structural engineering', 'تصميم ميكانيكي', 'هندسة ميكانيكية'],
        'electrical': ['electrical', 'robotics', 'هندسة كهربائية', 'أنظمة كهربائية'],
        'civil': ['civil engineering', 'building construction', 'هندسة مدنية'],
        'robotics': ['robotics', 'روبوتات', 'التحكم الآلي'],
        'advanced_mathematics': ['mathematics for engineers', 'applied mathematics', 'الرياضيات الهندسية']
    },
    'The law': {
        'criminal_law': ['criminal law', 'قانون جنائي', 'الجريمة'],
        'business_law': ['business law', 'قانون الأعمال', 'قانون الشركات'],
        'intellectual_property': ['intellectual property', 'حقوق الملكية الفكرية', 'براءات الاختراع'],
        'human_rights': ['human rights', 'حقوق الإنسان']
    },
    'Biology': {
        'genetics': ['genetics', 'علم الوراثة', 'DNA'],
        'ecology': ['ecology', 'علم البيئة', 'بيئة'],
        'cell_biology': ['cell biology', 'بيولوجيا الخلايا']
    },
    'Medicine': {
        'anatomy': ['anatomy', 'تشريح', 'الجهاز العظمي'],
        'pathology': ['pathology', 'علم الأمراض'],
        'clinical_neuroscience': ['neuroscience', 'علم الأعصاب', 'الجهاز العصبي'],
        'microbiology': ['microbiology', 'علم الميكروبات']
    }
}

# Book prices - default prices for each category with some variations
book_prices = {
    'IT': {
        'default': 34.99,
        'Python for Beginners': 29.99,
        'Artificial Intelligence: A Modern Approach': 49.99,
        'Deep Learning with Python': 42.99,
        'Machine Learning Yearning': 27.99
    },
    'Engineering': {
        'default': 39.99,
        'Advanced Engineering Mathematics': 47.99,
        'The Art of Electronics': 54.99
    },
    'The law': {
        'default': 42.99,
        'Criminal Law Handbook': 49.99
    },
    'Biology': {
        'default': 36.99,
        'Molecular Biology of the Cell': 54.99
    },
    'Medicine': {
        'default': 44.99,
        'Harrison\'s Principles of Internal Medicine': 64.99
    }
}

# Function to get book image URL from Google Books API
def get_book_image_url(book_title):
    """
    Fetch book cover image URL from Google Books API
    """
    api_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": book_title, "maxResults": 1}
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "items" in data and len(data["items"]) > 0:
            volume_info = data["items"][0]["volumeInfo"]
            # Prefer thumbnail image if available
            image_links = volume_info.get("imageLinks", {})
            thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail")
            if thumbnail:
                # Google Books URLs sometimes start with http, convert to https for safety
                return thumbnail.replace("http://", "https://")
    except Exception:
        pass
    # fallback image if not found
    return "https://via.placeholder.com/128x195?text=No+Image"

# Updated get_book_details to use the Google Books API image fetcher
def get_book_details(book_title, category):
    """Get all book details as a dictionary"""
    return {
        'title': book_title,
        'image_url': get_book_image_url(book_title),
        'price': get_book_price(book_title, category)
    }

# Function to get book price
def get_book_price(book_title, category):
    """Get the price for a book, or return a default one if not found"""
    if category in book_prices and book_title in book_prices[category]:
        return book_prices[category][book_title]
    elif category in book_prices:
        return book_prices[category]['default']
    else:
        return 35.99  # Default price if category not found

# Function to precisely determine the category based on keywords
def classify_category(query):
    query_lower = query.lower()
    for category, subcategories in category_keywords.items():
        for subcategory, keywords in subcategories.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return category, subcategory
    return "Unknown", None

# Function to search for books
def search_books(query, max_results=10):
    query_lower = query.lower()
    results = []
    
    # Get category and subcategory from keywords
    category, subcategory = classify_category(query)
    
    if category != "Unknown" and subcategory:
        # Return books from specific subcategory
        books_list = books_by_category.get(category, {}).get(subcategory, [])
        for book_title in books_list:
            book_details = get_book_details(book_title, category)
            results.append(book_details)
    else:
        # Search across all categories
        for category, subcategories in books_by_category.items():
            for subcategory, books_list in subcategories.items():
                for book_title in books_list:
                    if query_lower in book_title.lower():
                        book_details = get_book_details(book_title, category)
                        results.append(book_details)
                        if len(results) >= max_results:
                            break
                if len(results) >= max_results:
                    break
            if len(results) >= max_results:
                break
    
    return results[:max_results]

# Function to get book recommendations for a category
def get_book_recommendations(category, subcategory=None, max_results=5):
    results = []
    
    if subcategory and subcategory in books_by_category.get(category, {}):
        books_list = books_by_category[category][subcategory]
        for book_title in books_list[:max_results]:
            results.append(get_book_details(book_title, category))
    elif category in books_by_category:
        books_list = books_by_category[category].get('general', [])
        for book_title in books_list[:max_results]:
            results.append(get_book_details(book_title, category))
    
    return results