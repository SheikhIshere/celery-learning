## 🐍 **Backend (Django) – `README.md`**

````text
# AI Chat App Backend – Django + DRF + Gemini AI

This is the backend of a Fullstack AI Chat Application built with Django and Django REST Framework, integrated with **Gemini AI** (via Google Generative AI SDK). It provides a RESTful API for managing chat messages and communicating with Google's Gemini models.

## ⚙️ Tech Stack
- Python 3.x
- Django
- Django REST Framework
- Google Generative AI (Gemini)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/gemini_chat_app_backend.git
cd gemini_chat_app_backend
````

### 2. Create and Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure `google-generativeai` is listed in your `requirements.txt`.

### 4. Add Your Gemini API Key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

You'll get your key from [Google AI Studio](https://makersuite.google.com/app/apikey).
You can use `python-decouple` or access it via `os.environ`.

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Start the Server

```bash
python manage.py runserver
```

## 🧠 How It Works

* The frontend sends user messages to the Django backend
* Django uses the Gemini SDK to send prompts and receive responses
* Responses are streamed or returned and sent back to the frontend

```