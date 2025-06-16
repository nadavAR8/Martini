import pytest
from backend.find_best_models import find_best_models

def test_coding_query():
        query = "I need a model to help with writing Python code"
        result = find_best_models(query)
        assert result["catagory"] == "coding"

def test_medicine_query():
    query = "A language model for medical clinical notes or medicine"
    result = find_best_models(query)
    assert result["catagory"] == "medicine"
