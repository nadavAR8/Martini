import json
import os
from typing import List, Dict

def find_best_models(query: str, json_path: str = "backend/llm_catalog.json") -> list:
    """
    Loads the LLM catalog from a JSON file and returns the category that best
    matches the provided query using a simple keyword based approach. The top
    three models from that category are returned.

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

    # Basic keyword matching without external dependencies
    query_lower = query.lower()

    keyword_map: Dict[str, List[str]] = {
        "coding": ["code", "coding", "programming", "python", "developer"],
        "physics": ["physics", "quantum", "science", "atom", "space"],
        "medicine": ["medicine", "medical", "clinical", "health", "hospital"],
    }

    scores = {}
    for category in categories:
        keywords = keyword_map.get(category, [category])
        scores[category] = sum(query_lower.count(word) for word in keywords)

    best_category = max(scores, key=scores.get)

    return {
        "catagory": best_category,
        "models": catalog[best_category][:3],
    }

