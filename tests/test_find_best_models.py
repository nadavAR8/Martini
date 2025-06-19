import pytest
from backend.find_best_models import find_best_models

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