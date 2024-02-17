import spacy
import re

def extract_keywords(text, max_keywords=4):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")
    
    # Process the text with spaCy
    doc = nlp(text)

    # Extract keywords based on relevant criteria (e.g., noun phrases)
    keywords = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]

    # Keep only unique keywords
    keywords = list(set(keywords))

    # Sort keywords by frequency
    keyword_freq = {keyword: text.count(keyword) for keyword in keywords}
    sorted_keywords = sorted(keyword_freq, key=keyword_freq.get, reverse=True)

    # Limit the number of keywords
    keywords = sorted_keywords[:max_keywords]

    return keywords

