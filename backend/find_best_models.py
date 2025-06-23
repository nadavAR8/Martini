from sentence_transformers import SentenceTransformer, util
import json, os

import os
import json

def load_catalog(json_path: str = "llm_catalog.json") -> dict:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    catalog_path = os.path.join(script_dir, json_path)

    if not os.path.exists(catalog_path):
        raise FileNotFoundError(f"Catalog file not found at: {catalog_path}")

    with open(catalog_path, "r") as f:
        catalog = json.load(f)

    return catalog


def get_best_matching_category(query: str, categories: list[str]) -> str:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query, convert_to_tensor=True)
    category_embeddings = model.encode(categories, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(query_embedding, category_embeddings).squeeze()
    best_index = similarities.argmax().item()

    # print("\n🔍 Category Similarity Scores:")
    # for category, score in zip(categories, similarities):
    #    print(f"{category}: {score.item():.4f}")

    return categories[best_index]

def model_matches_filters(model: dict, filters: dict) -> bool:
    # Map of filter keys to handling functions
    filter_handlers = {
        "price_per_call": lambda m, v: v[0] <= m.get("price_per_call", float("inf")) <= v[1],
        "num_parameters": lambda m, v: v[0] <= m.get("num_parameters", 0) <= v[1],
        "context_window": lambda m, v: v[0] <= m.get("context_window", 0) <= v[1],
        "supports_fine_tuning": lambda m, v: m.get("supports_fine_tuning", False) == v,
        "open_source": lambda m, v: m.get("open_source", False) == v,
        "gpu_memory_requirement": lambda m, v: v[0] <= m.get("gpu_memory_requirement", float("inf")) <= v[1],
        "company": lambda m, v: m.get("company", "").lower() in [c.lower() for c in v],
        "huggingface": lambda m, v: m.get("huggingface", False) == v,
    }

    for key, value in filters.items():
        handler = filter_handlers.get(key)
        if handler and not handler(model, value):
            return False
    return True

def find_best_models(query: str, json_path: str = "llm_catalog.json", top_n: int = 3, advanced_filters: dict = None) -> dict:
    """
    Main function to find top_n models based on query and optional advanced filters.

    :param query: Natural language input from user
    :param json_path: Path to JSON catalog file
    :param top_n: Number of models to return
    :param advanced_filters: Optional dict of filters
    :return: Dict with category and list of model dicts
    """
    catalog = load_catalog(json_path)
    models = catalog["models"]

    # Get unique categories from models
    unique_categories = sorted({
        category
        for model in models
        for category in model.get("categories", [])
    })

    # Match category to query
    best_category = get_best_matching_category(query, unique_categories)

    # Filter models in that category
    filtered_models = [m for m in models if best_category in m.get("categories", [])]

    # Apply advanced filters
    if advanced_filters:
        filtered_models = [m for m in filtered_models if model_matches_filters(m, advanced_filters)]

    # Sort by bayesian_score (default to 0 if missing)
    top_models = sorted(filtered_models, key=lambda m: m.get("bayesian_score", 0), reverse=True)[:top_n]

    return {
        "category": best_category,
        "models": top_models
    }




if __name__ == "__main__":
    import sys
    query = sys.argv[1]
    result = find_best_models(query)
    print(json.dumps(result))  # Ensure it prints to stdout