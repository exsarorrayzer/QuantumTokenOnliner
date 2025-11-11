import websockets
import asyncio
import json

class WebSocketClient:
    def __init__(self, token, proxy=None):
        self.token = token
        self.proxy = proxy
        self.ws = None
    
    async def connect(self):
        pass
    
    async def keep_online(self):
        pass