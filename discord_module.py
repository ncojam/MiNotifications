# discord_module.py
import requests
import logging

# === SETTINGS ===
DISCORD_TOKEN = "your_discord_token"
DISCORD_THREAD_ID = 0

ENABLED = DISCORD_TOKEN != "your_discord_token" and DISCORD_THREAD_ID != 0

API_BASE = "https://discord.com/api/v10"

def send_message(content: str):
	if not ENABLED:
		return

	url = f"{API_BASE}/channels/{DISCORD_THREAD_ID}/messages"
	headers = {
		"Authorization": f"Bot {DISCORD_TOKEN}",
		"Content-Type": "application/json"
	}
	data = {"content": content}

	resp = requests.post(url, headers=headers, json=data)
	if resp.status_code not in (200, 201):
		logging.warning(f"Discord error: {resp.status_code} {resp.text}")
