from config import JOINERS_HUB_CHANNELS_ID # <--- ИЗМЕНЕНИЕ 1
import platform

if platform.system() == "Windows":
    import ctypes

def check_channel(channel_id: str):
    # Используем новое название переменной
    for tier, ids in JOINERS_HUB_CHANNELS_ID.items(): # <--- ИЗМЕНЕНИЕ 2
        if channel_id in ids:
            return True, tier
    return False, None


def parse_money(value: str) -> float:
    value = value.strip("*$ /s")
    if value.endswith("K"):
        return round(float(value[:-1]) / 1000, 3)
    elif value.endswith("M"):
        return round(float(value[:-1]), 3)
    elif value.endswith("B"):
        return round(float(value[:-1]) * 1000, 3)
    else:
        return 0.0


def extract_server_info(event: dict):
    result = {"name": None, "money": None, "script": None, "job_id": None, "players": None}

    try:
        embeds = event["d"].get("embeds", [])
        if not embeds:
            return result

        fields = embeds[0].get("fields", [])
        for field in fields:
            name = field.get("name", "").strip()
            value = field.get("value", "").strip()

            if name.startswith("🏷️ Name"):
                result["name"] = value.strip("*")

            elif name.startswith("💰 Money per sec"):
                result["money"] = parse_money(value.strip("*"))

            elif name.startswith("📜 Join Script (PC)"):
                result["script"] = value.strip("`")

            elif name.startswith("Job ID (PC)"):
                result["job_id"] = value.strip("`")

            elif name.startswith("👥 Players"):
                players_str = value.strip("*")
                current, _ = players_str.split("/")
                result["players"] = current

    except Exception as e:
        #print(f"Error parsing message: {e}")
        pass

    return result

def set_console_title(title: str):
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    return
              
