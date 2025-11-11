import time
from datetime import datetime

class StatisticsTracker:
    def __init__(self):
        self.start_time = time.time()
        self.requests_sent = 0
        self.successful_connections = 0
        self.failed_connections = 0
    
    def get_uptime(self):
        return time.time() - self.start_time
    
    def get_success_rate(self):
        total = self.successful_connections + self.failed_connections
        return (self.successful_connections / total * 100) if total > 0 else 0
    
    def update_data_json(self):
        pass