from qbittorrent import Client
from config import *
from change_doujinshi_subfolder import *

# 创建qbittorrent客户端实例
client = Client(QB_URL)

# 登录qbittorrent
try:
    client.login(username=QB_USER, password=QB_PASSWORD)
except Exception as e:
    print(f"Login failed: {e}")

# 获取所有活动的种子
torrents = client.torrents(category='Doujinshi')

change_doujinshi_subfolder_with_event(torrents, client)

change_doujinshi_subfolder_with_artist(torrents, client)
