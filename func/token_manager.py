import json
from pathlib import Path

class TokenManager:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent
        self.tokens_file = self.base_path / "db" / "tokens.json"
        self.tokens_data = self.load_tokens()
    
    def load_tokens(self):
        try:
            with open(self.tokens_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return self.create_default_tokens()
    
    def create_default_tokens(self):
        default_data = {
            "tokens": [],
            "statistics": {
                "total": 0,
                "valid": 0,
                "invalid": 0,
                "online": 0,
                "offline": 0
            }
        }
        self.save_tokens(default_data)
        return default_data
    
    def save_tokens(self, data=None):
        if data is None:
            data = self.tokens_data
        try:
            with open(self.tokens_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Token save error: {e}")
    
    def update_statistics(self):
        stats = self.tokens_data["statistics"]
        tokens = self.tokens_data["tokens"]
        
        stats["total"] = len(tokens)
        stats["valid"] = len([t for t in tokens if t.get("valid", False)])
        stats["invalid"] = len([t for t in tokens if not t.get("valid", True)])
        stats["online"] = len([t for t in tokens if t.get("online", False)])
        stats["offline"] = len([t for t in tokens if not t.get("online", True)])
        
        self.save_tokens()
    
    def add_token(self, token, note=""):
        new_token = {
            "token": token,
            "note": note,
            "valid": True,
            "online": False,
            "added_date": "2024-01-01"
        }
        
        self.tokens_data["tokens"].append(new_token)
        self.update_statistics()
        return True
    
    def remove_token(self, token):
        self.tokens_data["tokens"] = [t for t in self.tokens_data["tokens"] if t["token"] != token]
        self.update_statistics()
        return True
    
    def validate_token(self, token):
        # Token validation logic buraya gelecek
        for t in self.tokens_data["tokens"]:
            if t["token"] == token:
                t["valid"] = True
                self.update_statistics()
                return True
        return False
    
    def get_all_tokens(self):
        return self.tokens_data["tokens"]
    
    def get_valid_tokens(self):
        return [t for t in self.tokens_data["tokens"] if t.get("valid", False)]
    
    def get_online_tokens(self):
        return [t for t in self.tokens_data["tokens"] if t.get("online", False)]
    
    def set_online_status(self, token, online):
        for t in self.tokens_data["tokens"]:
            if t["token"] == token:
                t["online"] = online
                self.update_statistics()
                return True
        return False