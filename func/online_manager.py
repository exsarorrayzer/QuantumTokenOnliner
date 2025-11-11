import asyncio
import json
from pathlib import Path
from func.websocket_client import WebSocketClient
from func.token_manager import TokenManager

class OnlineManager:
    def __init__(self):
        self.token_manager = TokenManager()
        self.clients = []
        self.running = False
        self.config = self.load_config()
    
    def load_config(self):
        config_path = Path(__file__).resolve().parent.parent / "db" / "config.json"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    
    async def start_online(self):
        self.running = True
        tokens = self.token_manager.get_valid_tokens()
        
        tasks = []
        for token_data in tokens:
            client = WebSocketClient(token_data["token"], self.config)
            task = asyncio.create_task(client.keep_online())
            tasks.append(task)
            self.clients.append(client)
            
            threading_config = self.config.get("threading", {})
            delay = threading_config.get("delay_between", 0.1)
            await asyncio.sleep(delay)
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def stop_online(self):
        self.running = False
        for client in self.clients:
            asyncio.create_task(client.disconnect())
        self.clients.clear()
    
    def get_online_count(self):
        return len([client for client in self.clients if client.connected])
    
    def update_token_statuses(self):
        online_count = self.get_online_count()
        for i, client in enumerate(self.clients):
            if i < len(self.token_manager.tokens_data["tokens"]):
                token = self.token_manager.tokens_data["tokens"][i]["token"]
                self.token_manager.set_online_status(token, client.connected)