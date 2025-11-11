# 🔷 QuantumOnliner

**Quantum-Level Discord Token Online Tool**

A high-performance, multi-threaded Discord token online manager with advanced features and real-time monitoring.

## 🚀 Features

- **Multi-Token Support**: Manage thousands of Discord tokens simultaneously

- **WebSocket Connection**: Real-time Discord Gateway connections for each token

- **Proxy Support**: Residential, datacenter, and rotating proxy support

- **Configurable Presence**: Custom status, activities, and online status from config

- **Real-time Statistics**: Live monitoring of connections and performance

- **Auto-Rotation**: Automatic proxy and status rotation

- **Security Features**: User agent rotation, fingerprint spoofing, request randomization

## 📁 Project Structure

```

QuantumOnliner/
├──main.py                 # Main application entry point
├──db/                     # Database files
│├── config.json        # Application configuration
│├── data.json          # Application data and statistics
│├── proxy.json         # Proxy configurations
│└── tokens.json        # Token storage
└──func/                  # Function modules
├── banner.py          # Banner display system
├── creds.py           # Credits display
├── token_manager.py   # Token management
├── proxy_manager.py   # Proxy management
├── websocket_client.py # Discord WebSocket client
└── online_manager.py  # Online session management

```

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/exsarorrayzer/QuantumTokenOnliner
   cd QuantumTokenOnliner
```

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your settings
   · Edit db/config.json for application settings
   · Add proxies to db/proxy.json
   · Add tokens using the application menu

🛠️ Requirements

```txt
colorama>=0.4.6
pyfiglet>=0.8.post1
rich>=13.0.0
websockets>=12.0
aiohttp>=3.9.0
```

🎮 Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Main Menu Options:
   · Token Management: Add, remove, and validate tokens
   · Proxy Management: Configure proxy servers
   · Start Online: Begin online session with all tokens
   · Statistics: View real-time performance metrics
   · Settings: Configure application behavior
3. Adding Tokens:
   Use the token management menu to add Discord tokens with optional notes.
4. Proxy Configuration:
   Support for multiple proxy types with automatic rotation.

⚡ Configuration

Edit db/config.json to customize:

```json
{
  "discord": {
    "status": "online",
    "custom_status": "QuantumOnliner",
    "status_rotation": true
  },
  "threading": {
    "max_workers": 50,
    "delay_between": 0.1
  }
}
```

🔧 Features Detail

Token Management

· Bulk token operations
· Token validation
· Online/offline status tracking
· Note system for organization

Proxy System

· Multiple proxy types (residential, datacenter, rotating)
· Geographic distribution
· Automatic failover
· Performance monitoring

WebSocket Client

· Stable Discord Gateway connections
· Heartbeat management
· Presence customization
· Error handling and reconnection

📊 Statistics

Real-time monitoring includes:

· Total tokens and online count
· Connection success rates
· Proxy performance metrics
· System resource usage

⚠️ Disclaimer

This tool is for educational and research purposes only. Users are responsible for complying with Discord's Terms of Service and applicable laws. The developers are not responsible for any misuse of this software.

👨‍💻 Developer

exsarorrayzer

· GitHub: @exsarorrayzer
· Instagram: @exsarorrayzer
· YouTube: @exsarorrayzer

📄 License

This project is for educational purposes. Use responsibly and in compliance with all applicable terms of service and laws.

---

QuantumOnliner - Professional Discord Token Management Solution

```