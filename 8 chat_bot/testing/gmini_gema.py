import os
from dotenv import load_dotenv
from google import genai
load_dotenv()

while True:
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    user_input = input("me: ")
    if user_input.lower() == 'stop':
        break
    try:
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=user_input,
        )
        print(f"ai: {response.text}")
    except Exception as e:
        print(f"error: {e}")






