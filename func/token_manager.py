import json
from pathlib import Path

class TokenManager:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent
        self.tokens_file = self.base_path / "db" / "tokens.json"
        self.tokens = self.load_tokens()
    
    def load_tokens(self):
        try:
            with open(self.tokens_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"tokens": [], "statistics": {"total": 0, "valid": 0, "invalid": 0}}
    
    def update_statistics(self):
         pass