import asyncio
import logging
from datetime import datetime, timedelta

from mcstatus import JavaServer
from telegram import Bot

# === SETTINGS ===
SERVER_IP = "your server IP"
CHECK_INTERVAL = 10  # secons
TELEGRAM_TOKEN = "your token"
CHAT_ID = -1002222333444  # your chat_id
COOLDOWN_HOURS = 2

# === INITIALIZATION ===
bot = Bot(token=TELEGRAM_TOKEN)
server = JavaServer.lookup(SERVER_IP)

cooldowns = {}  # {nickname: last login datetime}

logging.basicConfig(level=logging.INFO)

async def check_server():
	while True:
		try:
			status = server.status()
			now = datetime.now()

			if status.players.sample:
				for player in status.players.sample:
					name = player.name
					last_seen = cooldowns.get(name)

					if not last_seen or now - last_seen > timedelta(hours=COOLDOWN_HOURS):
						await bot.send_message(chat_id=CHAT_ID, text=f"🎮 Player {name} joined the server!")
						cooldowns[name] = now
			else:
				logging.info("Server's empty.")

		except Exception as e:
			logging.warning(f"Error parsing server: {e}")

		await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
	asyncio.run(check_server())
