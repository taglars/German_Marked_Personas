from generators.openai_gen import generate_openai_personas
from config import DEMOGRAPHICS, PROMPTS
import json
import os

def generate_demographic_data(demographic, gender):
    """Generate data for a specific demographic group"""
    texts = []
    for prompt in PROMPTS:
        formatted_prompt = prompt.format(demographic=f"{demographic} {gender}")
        # Generate 15 personas per prompt
        response = generate_openai_personas(formatted_prompt, n_samples=15)
        texts.extend(response)
    return texts

def main():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Generate and save data for each demographic group
    for background, gender in DEMOGRAPHICS:
        print(f"Generating personas for {background} {gender}...")
        texts = generate_demographic_data(background, gender)
        
        # Save raw generations
        filename = f"{background}_{gender}_raw.json"
        with open(f'data/{filename}', 'w', encoding='utf-8') as f:
            json.dump(texts, f, ensure_ascii=False, indent=4)
        
        print(f"Saved {len(texts)} personas to {filename}")

if __name__ == "__main__":
    main()
