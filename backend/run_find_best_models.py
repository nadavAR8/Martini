import sys
import json
from find_best_models import find_best_models

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided"}))
        sys.exit(1)
    query = sys.argv[1]
    result = find_best_models(query)
    print(json.dumps(result))
