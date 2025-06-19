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

    print("\n🔍 Category Similarity Scores:")
    for category, score in zip(categories, similarities):
        print(f"{category}: {score.item():.4f}")

    return categories[best_index]



def find_best_models(query: str, json_path: str = "llm_catalog.json", top_n: int = 3) -> dict:
    catalog = load_catalog(json_path)
    models = catalog["models"]

    # Build unique category list
    unique_categories = sorted({
        category
        for model in models
        for category in model.get("categories", [])
    })

    # Semantic category matching
    best_category = get_best_matching_category(query, unique_categories)

    # Get top 3 models in best category by Bayesian score
    filtered_models = [
        m for m in models if best_category in m.get("categories", [])
    ]
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