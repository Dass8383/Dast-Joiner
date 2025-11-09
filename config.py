DISCORD_TOKEN = ""
# discord token / дискорд токен
# гайд/guide: https://www.youtube.com/results?search_query=how+to+get+discord+token


MONEY_THRESHOLD = (15.0, 9999.0) # in millions from, to / в миллионах от, до (example: 1.5 = 1.5m, 0.5 = 500k)
# if the brainrot earnings per second are less than the first number or higher than the second number, it will be skipped
# если заработок в секунду у брейнрота меньше первого числа или выше второго числа, то он будет скипнут
# Example / Пример: (3.0, 10.0) - от 3м до 10м / from 3m to 10m


PLAYER_TRESHOLD = 8 # число / number
# if there are more PLAYER_TRESHOLD players on the server - it will not try to enter the server
# если на сервере больше PLAYER_TRESHOLD игроков - не будет пытаться зайти на сервер


IGNORE_UNKNOWN = False # True / False
# ignore "Unknown" brainrots
# игнорировать "Unknown" брейнротов


IGNORE_LIST = [""] # ignore list, список игнора
# Добавьте имена брейнротов в данный список которых надо скипать
# Add the names of the brainrots to this list of those that need to be skipped
# Example 1 / Пример 1: ["Graipuss Medussi"]
# Example 2 / Пример 2: ["Graipuss Medussi", "La Grande Combinasion"]


FILTER_BY_NAME = False, ["Graipuss Medussi", "La Grande Combinasion"] # filter by name, фильтр по имени
# Что-бы он работал, поменяйте False на True, а также в список добавьте\уберите\измените название необходимых брейнротов
# To make it work, change False to True, and add/remove/change the names of the necessary brainroots to the list
# Если включено: будет заходить на сервера где название брейнрота соответствует списку
# If enabled: will connect to servers where the brainrot name matches the list
# Example/пример: True, ["Graipuss Medussi"]


BYPASS_10M = True # True / False


READ_CHANNELS = ['rexzy-notif'"] # channels / каналы
# список каналов логов какие читать (айдишники снизу)
# list of log channels to read (IDs at the bottom)
# Don't change it if you don't know what you're doing.
# не меняйте если не понимаете что делаете





# DON'T TOUCH ! / НЕ ТРОГАЙ !
# don't touch it if you don't understand what it is / не трогай если не понимаешь что это
WEBSOCKET_PORT = 51948 # websocket port for data transfer in roblox

DISCORD_WS_URL = "wss://gateway.discord.gg/?encoding=json&v=9" # discord ws

JOINERS_HUB_CHANNELS_ID = {
    "rexzy-notif": ["1426620552407416973"]
}
