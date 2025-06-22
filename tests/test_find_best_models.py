import pytest
from backend.find_best_models import find_best_models
from backend.find_best_models import load_catalog

@pytest.fixture
def model_catalog():
    json_path = "llm_catalog.json"
    catalog = load_catalog(json_path)
    return catalog

def test_coding_query():
        query = "I need a model that will help be building my application"
        result = find_best_models(query)
        assert result["category"] == "coding & programming"

def test_medicine_query():
    query = "I want to built a nice application to help breast cancer patients"
    result = find_best_models(query)
    assert result["category"] == "medical & health"

def test_physics_query():
    query = "I need a model to help with quantum physics research"
    result = find_best_models(query)
    assert result["category"] == "physics"
    assert len(result["models"]) == 3  # Ensure we get top 3 models
    for model in result["models"]: print(model["model_name"])

def test_advanced_filter_supports_fine_tuning():
    query = "I want to summarize medical texts"
    filters = {
        "supports_fine_tuning": True
    }
    result = find_best_models(query, advanced_filters=filters)
    assert all(model["advanced_filters"]["supports_fine_tuning"] for model in result["models"])

def test_advanced_filter_company_and_price():
    query = "I need a language model for finance analysis"
    filters = {
        "company": ["Meta", "Google", "Microsoft"],
        "price_per_call": (0.0, 0.005)
    }
    result = find_best_models(query, advanced_filters=filters)
    for model in result["models"]:
        adv = model["advanced_filters"]
        assert adv["company"] in filters["company"]
        assert filters["price_per_call"][0] <= adv["price_per_call"] <= filters["price_per_call"][1]
