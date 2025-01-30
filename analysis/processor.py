def process_texts(texts):
    """Process and clean the generated texts"""
    if not texts:
        return []
    
    # Basic text cleaning
    processed_texts = []
    for text in texts:
        # Remove special characters
        cleaned_text = text.replace('\n', ' ').strip()
        # Remove multiple spaces
        cleaned_text = ' '.join(cleaned_text.split())
        processed_texts.append(cleaned_text)
    
    return processed_texts
