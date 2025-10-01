import os
from dotenv import load_dotenv
import cohere

load_dotenv()

co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

def generate_text(prompt, model="command-r-plus-08-2024"):
    response = co.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.message.content[0].text
