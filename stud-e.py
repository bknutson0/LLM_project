import os
import openai

api_key = os.environ.get('OPENAI_API_KEY')

if not api_key:
    raise ValueError("API key not found in environment variables!")

print(api_key)