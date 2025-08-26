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
THREAD_ID = 3 # your thread_id
COOLDOWN_HOURS = 1

# === INITIALIZATION ===
bot = Bot(token=TELEGRAM_TOKEN)
server = JavaServer.lookup(SERVER_IP)

player_status = {}  # {nickname: (online: bool, last_notification: datetime)}
initial_check_done = False  # Last check completion flag

logging.basicConfig(level=logging.INFO)

async def check_server():
    global initial_check_done
    
    while True:
        try:
            status = server.status()
            now = datetime.now()
            current_players = {p.name for p in status.players.sample} if status.players.sample else set()

            # First check - only save status
            if not initial_check_done:
                for name in current_players:
                    player_status[name] = (True, None)  # Save online-status with no notification
                logging.info(f"Initial check: {len(current_players)} players online")
                initial_check_done = True
                await asyncio.sleep(CHECK_INTERVAL)
                continue
            
            # Next checks - regular procedure
            all_players = set(player_status.keys()).union(current_players)
            
            for name in all_players:
                is_online = name in current_players
                last_data = player_status.get(name, (False, None))
                was_online, last_notification = last_data
                
                if is_online and not was_online:  # Player joined
                    if last_notification is None or (now - last_notification) > timedelta(hours=COOLDOWN_HOURS):
                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=f"🎮 Player {name} joined the server!",
                            reply_to_message_id=THREAD_ID # Remove this if you need to post to general
                        )
                        player_status[name] = (True, now)
                    else:
                        player_status[name] = (True, last_notification)
                elif not is_online:  # Игрок вышел
                    player_status[name] = (False, last_notification)

            logging.info(f"Check complete. Online: {len(current_players)} players.")

        except Exception as e:
            logging.warning(f"Error parcing the server: {e}")

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(check_server())
