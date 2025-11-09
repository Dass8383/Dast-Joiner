# main.py (или discord.py)

import asyncio
import websockets
import websockets.exceptions
import json
import random

from src.logger.logger import setup_logger
from config import (DISCORD_WS_URL, DISCORD_TOKEN, MONEY_THRESHOLD,
                    IGNORE_UNKNOWN, PLAYER_TRESHOLD, BYPASS_10M,
                    FILTER_BY_NAME, IGNORE_LIST, READ_CHANNELS)
from server import server
from utils import check_channel, extract_server_info, set_console_title

logger = setup_logger()

# ВАШИ ID КАНАЛОВ, которые используются для подписки на события Discord
CHANNEL_ID_TIER1 = "1408834071752216648"
CHANNEL_ID_TIER2 = "1426620552407416973"


async def identify(ws):
    identify_payload = {
        "op": 2,
        "d": {
            "token": DISCORD_TOKEN,
            "properties": {
                "os": "Windows", "browser": "Chrome", "device": "", "system_locale": "en-US",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
                "referrer": "https://discord.com/", "referring_domain": "discord.com"
            }
        }
    }

    await ws.send(json.dumps(identify_payload))
    logger.info("Sent client identification")

    # --- ИСПРАВЛЕННАЯ ПОДПИСКА НА ВАШИ КАНАЛЫ (Op 37) ---
    payload = {
        "op": 37,
        "d": {
            "subscriptions": {
                # Подписка на ваш Tier 1 ID
                CHANNEL_ID_TIER1: {"typing": True, "threads": True, "activities": True, "members": [], "member_updates": False, "channels": {}, "thread_member_lists": []},
                # Подписка на ваш Tier 2 ID
                CHANNEL_ID_TIER2: {"typing": True, "threads": True, "activities": True, "members": [], "member_updates": False, "channels": {}, "thread_member_lists": []}
            }
        }
    }
    await ws.send(json.dumps(payload))
    logger.info("Sent client subscriptions to your channels.")
    logger.info("You are using a custom AutoJoiner setup.")
# ------------------------------------------------------------------------


async def message_check(event):
    channel_id = event['d']['channel_id']
    result, category = check_channel(channel_id)
    if result:
        try:
            parsed = extract_server_info(event)
            if not parsed: return

            # Логика фильтрации (деньги, игроки, игнор-листы)
            if parsed['money'] < MONEY_THRESHOLD[0] or parsed['money'] > MONEY_THRESHOLD[1]:
                return

            if category not in READ_CHANNELS:
                return

            if parsed['name'] == "Unknown" and IGNORE_UNKNOWN:
                logger.warning("Skipped unknown server.")
                return

            if int(parsed['players']) >= PLAYER_TRESHOLD:
                logger.warning(f"Skipped server {parsed['players']} >= {PLAYER_TRESHOLD} players.")
                return

            if FILTER_BY_NAME[0]:
                if parsed['name'] not in FILTER_BY_NAME[1]:
                    logger.warning(f"Skip server {parsed['name']} not in filter by name list.")
                    return

            if parsed['name'] in IGNORE_LIST:
                logger.warning(f"Skip server {parsed['name']} in ignore list.")
                return

            # Логика отправки в игру
            if parsed['money'] >= 10.0:
                if not BYPASS_10M:
                    logger.warning("Skip 10m+ server because bypass turned off.")
                    return

                await server.broadcast(parsed['job_id'])
            else:
                await server.broadcast(parsed['script'])
            logger.info(f"Sent {parsed['name']} in category {category}: {parsed['money']} M/s.")

            # Убрано рекламное сообщение
        except Exception as e:
            logger.debug(f"Failed to check message: {e}")

async def message_listener(ws):
    logger.info("Listening new messages...")
    while True:
        event = json.loads(await ws.recv())
        op_code = event.get("op", None)

        if op_code == 0: # Dispatch
            event_type = event.get("t")

            if event_type == "MESSAGE_CREATE" and not server.paused:
                await message_check(event)

        elif op_code == 9: # Invalid Session
            logger.warning("The session has ended, creating a new one..")
            await identify(ws)


async def listener():
    set_console_title(f"AutoJoiner | Status: Enabled")
    while True:
        try:
            async with websockets.connect(DISCORD_WS_URL, max_size=None) as ws:
                await identify(ws)
                await message_listener(ws)

        except websockets.exceptions.ConnectionClosed as e:
            logger.error(f" - WebSocket closed with error: {e}. Trying to reconnect... (check your discord token)")
            await asyncio.sleep(3)
            continue


def main():
    """Основная точка входа для запуска всего приложения."""
    from server import roblox_main # Импортируем функцию запуска сервера
    import threading
    import time
    
    # 1. Запуск WebSocket-сервера в отдельном потоке
    roblox_thread = threading.Thread(target=roblox_main, daemon=True)
    roblox_thread.start()
    logger.info("Websocket server thread initiated.")
    
    # Даем немного времени для запуска WebSocket-сервера
    time.sleep(1)

    # 2. Запуск Discord-клиента (блокирует основной поток)
    try:
        asyncio.run(listener())
    except Exception as e:
        logger.critical(f"Failed to start Discord Listener. Check DISCORD_TOKEN in config.py. Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()
      
