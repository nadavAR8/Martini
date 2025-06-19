import json
import os
from find_best_models import load_catalog

def compute_bayesian_score(rating, votes, global_avg, min_votes=10000):
    return (votes / (votes + min_votes)) * rating + (min_votes / (votes + min_votes)) * global_avg

def update_model_rating(model: dict, new_user_rating: float) -> dict:
    current_avg = model["stars_ranking"]
    count = model["number_of_ratings"]
    
    updated_count = count + 1
    updated_avg = ((current_avg * count) + new_user_rating) / updated_count

    model["stars_ranking"] = round(updated_avg, 4)
    model["number_of_ratings"] = updated_count
    return model

def update_global_avg(global_stats: dict, new_user_rating: float) -> dict:
    total = global_stats["total_ratings"]
    avg = global_stats["global_avg_rating"]

    new_total = total + 1
    new_avg = ((avg * total) + new_user_rating) / new_total

    global_stats["total_ratings"] = new_total
    global_stats["global_avg_rating"] = round(new_avg, 4)
    return global_stats


def process_model_rating(model_name: str, new_user_rating: float, json_path: str = "llm_catalog.json"):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), json_path)
    catalog = load_catalog(json_path)

    # Find model
    model = next((m for m in catalog["models"] if m["model_name"] == model_name), None)
    if model is None:
        raise ValueError(f"Model '{model_name}' not found in catalog.")

    # Update model average and rating count
    model = update_model_rating(model, new_user_rating)

    # Update global average
    catalog["global_stats"] = update_global_avg(catalog["global_stats"], new_user_rating)

    # Recompute Bayesian score
    model["bayesian_score"] = round(
        compute_bayesian_score(
            model["stars_ranking"],
            model["number_of_ratings"],
            catalog["global_stats"]["global_avg_rating"]
        ),
        4
    )

    # Save updated file
    with open(path, "w") as f:
        json.dump(catalog, f, indent=4)

    print(f"Model '{model_name}' updated. New Bayesian score: {model['bayesian_score']}")
    return catalog  # Optional: Return updated category views

