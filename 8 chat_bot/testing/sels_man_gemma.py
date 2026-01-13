import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Initialize client once
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

# Define your salesman instructions here

product = {
    'id':'12fs34kldsfjl2ifuodsz1',
    'name':'nixxon zr1',
    'size':['s','m','ml','l','xl', 'xxl'],
    'color':['red', 'yellow', 'green', 'purple'],
    'stock':50,
    'price': 4999,
}

SALES_PERSONA = (
    "SYSTEM: you are a sales man of 'BATA' shoe company as customer care service "
    "Your goal is to sell out latest Shoe 'named nixxon zr1' and use 'Sir/Madam'. to address politely\n\n"
)

print("Salesman is ready. Type 'stop' to exit.")

while True:
    user_input = input("me: ")
    if user_input.lower() == 'stop':
        break
    
    try:
        # Combine the Persona + User Input into one string
        full_prompt = f"{SALES_PERSONA}User Question: {user_input} about product: {product}"
        
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=full_prompt,  # Send everything as one 'user' message
        )
        print(f"ai: {response.text}")
        
    except Exception as e:
        print(f"error: {e}")