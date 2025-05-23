# MiNotifications
**MiNotifications** is a Telegram bot that notifies you when a player joins your private Minecraft server. It periodically checks the server using `mcstatus` and sends a message to your private Telegram channel with the player's name.

## 🔧 Features

- Minecraft Java server player join notifications
- Cooldown system to avoid repeated messages from the same player
- Telegram bot integration
- Optional bash script for easier launch on Linux

---

## 🛠️ Setup Guide

### Step 1: Create a Telegram Bot

Go to [BotFather](https://telegram.me/BotFather), follow the instructions to create a new bot, and get your `TELEGRAM_TOKEN`.

---

### Step 2: Set up the Python environment

> Linux instructions (recommended):

```bash
python -m venv minotif
source minotif/bin/activate
pip install mcstatus python-telegram-bot requests
```

> Windows instructions:

```powerhell
python -m venv minotif
minotif\Scripts\activate
pip install mcstatus python-telegram-bot requests
```

### Step 3: Get your private channel chat ID

To find your Telegram private channel's chat_id:

- Log in to the [web version of Telegram](https://web.telegram.org/)
- Open your channel
- Look at the URL: `https://web.telegram.org/a/#-1002223334455`
- The `-1002223334455` part is your `chat_id`
- If your channel ID doesn’t start with `-100`, just add it manually as a prefix

### Step 4: Configure `server_monitor.py`

Open the script and change these settings:

```python
SERVER_IP = "your.minecraft.server:port"
CHECK_INTERVAL = 10  # seconds between server checks
TELEGRAM_TOKEN = "your_telegram_bot_token"
CHAT_ID = -100xxxxxxxxxx  # your channel's chat ID
COOLDOWN_HOURS = 2  # cooldown to avoid join-spam from the same player
```

### Step 5: Add bot as Admin to your channel

Add bot as Admin to your channel, make sure it does have access to channel's messages.

### Step 6: Run the monitor

> Linux:

```bash
source minotif/bin/activate
python server_monitor.py
```

Alternatively, make the helper script executable and run it:

```bash
chmod +x run_monitor.sh
./run_monitor.sh
```

> Windows:

```powershell
minotif\Scripts\activate
python server_monitor.py
```
