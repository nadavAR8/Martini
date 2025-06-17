import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def find_best_models(query: str, json_path: str = "llm_catalog.json") -> list:
    """
    Loads the LLM catalog from a JSON file, finds the best matching category 
    for the given query using cosine similarity, and returns the top 3 models.

    :param query: A string describing the user’s intent or use case
    :param json_path: Path to the JSON catalog file (default: "llm_catalog.json")
    :return: List of top 3 matching model dictionaries
    """
    # Load catalog from JSON
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Catalog file not found: {json_path}")
    
    with open(json_path, "r") as f:
        catalog = json.load(f)

    categories = list(catalog.keys())

    # Compute similarity between query and category names
    vectorizer = TfidfVectorizer() 
    tfidf_matrix = vectorizer.fit_transform([query] + categories)

    query_vec = tfidf_matrix[0]
    category_vecs = tfidf_matrix[1:]

    similarities = cosine_similarity(query_vec, category_vecs).flatten()
    best_category = categories[similarities.argmax()]

    return {"catagory": best_category, "models": catalog[best_category][:3]}  # Return top 3 models

if __name__ == "__main__":
    import sys
    query = sys.argv[1]
    result = find_best_models(query)
    print(json.dumps(result))  # Ensure it prints to stdout