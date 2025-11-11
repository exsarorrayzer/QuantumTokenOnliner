import websockets
import asyncio
import json
import time
from pathlib import Path

class WebSocketClient:
    def __init__(self, token, config):
        self.token = token
        self.config = config
        self.ws = None
        self.connected = False
        self.last_heartbeat = None
        self.sequence = None
    
    async def connect(self):
        try:
            headers = {
                "Authorization": self.token,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            self.ws = await websockets.connect(
                "wss://gateway.discord.gg/?v=9&encoding=json",
                extra_headers=headers
            )
            
            await self.identify()
            self.connected = True
            return True
            
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    async def identify(self):
        discord_config = self.config.get("discord", {})
        
        identify_payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "windows",
                    "$browser": "chrome",
                    "$device": "desktop"
                },
                "presence": {
                    "status": discord_config.get("status", "online"),
                    "since": 0,
                    "activities": self.get_activities(),
                    "afk": False
                }
            }
        }
        
        await self.ws.send(json.dumps(identify_payload))
    
    def get_activities(self):
        discord_config = self.config.get("discord", {})
        activities = discord_config.get("activities", [])
        
        if activities:
            return activities
        
        custom_status = discord_config.get("custom_status", "QuantumOnliner")
        if custom_status:
            return [{
                "name": "Custom Status",
                "type": 4,
                "state": custom_status
            }]
        
        return []
    
    async def heartbeat(self, interval):
        while self.connected:
            try:
                heartbeat_payload = {
                    "op": 1,
                    "d": self.sequence
                }
                await self.ws.send(json.dumps(heartbeat_payload))
                self.last_heartbeat = time.time()
                await asyncio.sleep(interval / 1000)
            except Exception as e:
                print(f"Heartbeat error: {e}")
                break
    
    async def listen(self):
        try:
            async for message in self.ws:
                data = json.loads(message)
                
                if data["op"] == 10:
                    interval = data["d"]["heartbeat_interval"]
                    asyncio.create_task(self.heartbeat(interval))
                
                elif data["op"] == 0:
                    self.sequence = data["s"]
                    
                    if data["t"] == "READY":
                        print(f"Connected: {self.token[:20]}...")
                
                elif data["op"] == 11:
                    pass
                    
        except Exception as e:
            print(f"Listen error: {e}")
        finally:
            self.connected = False
    
    async def keep_online(self):
        if await self.connect():
            await self.listen()
    
    async def disconnect(self):
        self.connected = False
        if self.ws:
            await self.ws.close()