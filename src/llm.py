from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def get_embeddings(text: str):
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = text
    )

    return response.data[0].embedding

def answer_question(question: str, context: str): 
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages = [
            {
                "role": "system",
                "content": "Odpovídej pouze na základě poskytnutého kontextu. "
                           "Pokud odpověď není v kontextu obsažena, odpověz: "
                           "Odpověď se v poskytnutých dokumentech nenachází "
            },
            {
                "role": "user",
                "content": f"Otázka: {question}\n\nKontext: {context}"
            }
        ]
    )

    return response.choices[0].message.content