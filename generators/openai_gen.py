from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from config import GENERATION_PARAMS


def generate_openai_personas(demographic, n_samples=5):
    """Generate descriptions for a demographic group using OpenAI API"""
    client = OpenAI(api_key=OPENAI_API_KEY)
    personas = []
    
    for _ in range(n_samples):  # 5 Versuche pro Prompt
        try:
            response = client.chat.completions.create(
                model="GPT-4o-2024-08-06", # change to "GPT-3.5-turbo-0125" in order to produce older Models Personas

                messages=[{
                    "role": "user",
                    "content": demographic
                }],
                **GENERATION_PARAMS
            )
            personas.append(response.choices[0].message.content)
            time.sleep(1)  # Rate Limiting
        except Exception as e:
            print(f"Error generating description: {e}")
    
    return personas
