import json
from pathlib import Path

class ProxyManager:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent
        self.proxy_file = self.base_path / "db" / "proxy.json"
        self.proxies = self.load_proxies()
    
    def load_proxies(self):
        try:
            with open(self.proxy_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return self.create_default_proxies()
    
    def create_default_proxies(self):
        default_data = {
            "residential": [],
            "datacenter": [],
            "rotating": [],
            "settings": {
                "default_type": "residential",
                "auto_rotate": True,
                "rotate_interval": 300,
                "max_retries": 3,
                "timeout": 10,
                "check_proxies": True,
                "ban_avoidance": True
            },
            "statistics": {
                "total_proxies": 0,
                "active_proxies": 0,
                "residential_count": 0,
                "datacenter_count": 0,
                "rotating_count": 0,
                "success_rate": 0
            }
        }
        self.save_proxies(default_data)
        return default_data
    
    def save_proxies(self, data=None):
        if data is None:
            data = self.proxies
        try:
            with open(self.proxy_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Proxy save error: {e}")
    
    def update_statistics(self):
        stats = self.proxies["statistics"]
        
        residential_count = len([p for p in self.proxies["residential"] if p.get("active", False)])
        datacenter_count = len([p for p in self.proxies["datacenter"] if p.get("active", False)])
        rotating_count = len([p for p in self.proxies["rotating"] if p.get("active", False)])
        
        stats["residential_count"] = residential_count
        stats["datacenter_count"] = datacenter_count  
        stats["rotating_count"] = rotating_count
        stats["active_proxies"] = residential_count + datacenter_count + rotating_count
        stats["total_proxies"] = len(self.proxies["residential"]) + len(self.proxies["datacenter"]) + len(self.proxies["rotating"])
        
        self.save_proxies()
    
    def add_proxy(self, proxy_type, ip, port, username, password, country, active=True):
        new_proxy = {
            "ip": ip,
            "port": port,
            "username": username,
            "password": password,
            "country": country,
            "active": active
        }
        
        if proxy_type in self.proxies:
            self.proxies[proxy_type].append(new_proxy)
            self.update_statistics()
            return True
        return False
    
    def remove_proxy(self, proxy_type, ip, port):
        if proxy_type in self.proxies:
            self.proxies[proxy_type] = [p for p in self.proxies[proxy_type] if not (p["ip"] == ip and p["port"] == port)]
            self.update_statistics()
            return True
        return False
    
    def get_active_proxies(self, proxy_type=None):
        if proxy_type:
            return [p for p in self.proxies.get(proxy_type, []) if p.get("active", False)]
        else:
            all_proxies = []
            for p_type in ["residential", "datacenter", "rotating"]:
                all_proxies.extend([p for p in self.proxies.get(p_type, []) if p.get("active", False)])
            return all_proxies
    
    def toggle_proxy(self, proxy_type, ip, port, active):
        if proxy_type in self.proxies:
            for proxy in self.proxies[proxy_type]:
                if proxy["ip"] == ip and proxy["port"] == port:
                    proxy["active"] = active
                    self.update_statistics()
                    return True
        return False