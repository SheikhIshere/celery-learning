import os
import google.generativeai as genai

# 1. Setup
genai.configure(api_key='AIzaSyBJal0fYDg8NnzVoAgQNm7SSChLIE6rprs')

# 2. Recommended: Use the 2026 stable model 'gemini-2.5-flash'
# Alternatively, use 'gemini-flash-latest' to always point to the current workhorse.
MODEL_NAME = 'gemini-2.5-flash' 

try:
    model = genai.GenerativeModel(MODEL_NAME)
    print(f"Connected to {MODEL_NAME}")
except Exception as e:
    print(f"Could not initialize {MODEL_NAME}: {e}")

print("Gemini AI Chat started. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    try:
        # Gemini 2.5+ uses generate_content
        response = model.generate_content(user_input)
        print("Bot:", response.text)
        
    except Exception as e:
        # If you still get a 404, this will help you see your available models
        if "404" in str(e):
            print("\n[Error] Model not found. Here are the models your key can access:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f" - {m.name}")
        else:
            print("Error:", e)