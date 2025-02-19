import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("twitter.env")

# Fetch API keys from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validate API keys
if not OPENAI_API_KEY:
    raise ValueError("\u274c OPENAI_API_KEY is missing! Please check your twitter.env file.")
if not GROQ_API_KEY:
    raise ValueError("\u274c GROQ_API_KEY is missing! Please check your twitter.env file.")

print("✅ OpenAI & Groq API keys loaded successfully!")

# Example function to test API keys
def test_openai():
    import openai
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, how are you?"}]
        )
        print("OpenAI Response:", response["choices"][0]["message"]["content"])
    except Exception as e:
        print("❌ OpenAI API Error:", e)

def test_groq():
    import requests
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"query": "Hello, how are you?"}
    try:
        response = requests.post("https://api.groq.com/test", headers=headers, json=data)
        print("Groq Response:", response.json())
    except Exception as e:
        print("❌ Groq API Error:", e)

# Run API tests
test_openai()
test_groq()
