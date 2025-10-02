import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def get_llm_response(prompt, language="Python"):
    """
    Send prompt to Groq LLM and get response
    """
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that provides code in {language}."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile"
    )
    return response.choices[0].message.content


