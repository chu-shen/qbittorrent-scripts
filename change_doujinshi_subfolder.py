import re
import os
from config import *


def change_doujinshi_subfolder_with_event(torrents, client):
    '''
    在当前目录下创建Event子目录，并将所有匹配Event的种子路径更改为Event子目录
    '''
    # 循环所有种子
    for torrent in torrents:
        # 获取种子名称
        name = torrent["name"]

        # 获取种子下载路径
        download_path = torrent["save_path"]

        # 跳过路径中包含特定字符串的种子。比如这里Artist的子目录下无需再创建Event子目录
        for word in SKIP_PATH:
            if word in download_path:
                flag = True
                break
        if flag:
            # client.set_torrent_location(torrent["hash"], download_path.replace(event, ""))
            continue

        # 使用正则表达式匹配
        match = re.search(EVENT_REGEX, name)

        if match:
            event = match.group(0)

            # 检查路径是否已包含前缀子目录
            if not download_path.endswith(event):
                # 在路径末尾添加前缀子目录
                new_download_path = f"{download_path}/{event}/"

                print("Change subfolder of: ", name,
                      " to: ", new_download_path)

                # 修改种子下载路径
                client.set_torrent_location(torrent["hash"], new_download_path)


def change_doujinshi_subfolder_with_artist(torrents, client):
    '''
    将指定艺术家的种子路径更改为艺术家子目录
    '''
    # 循环所有种子
    for torrent in torrents:
        # 获取种子名称
        name = torrent["name"]

        # 获取种子下载路径
        download_path = torrent["save_path"]

        for word in SKIP_PATH:
            if word in download_path:
                flag = True
                break
        if flag:
            continue

        # 使用正则表达式匹配
        match = re.search(ARTIST_REGEX, name)

        if match:
            artist = match.group(0)

            # 匹配团体/艺术家，作为艺术家下的子目录名
            group_artist = re.search(r'\[(.*?'+artist+r'.*?)\]', name)
            if group_artist:
                subdir_name = group_artist.group(1)
            else:
                subdir_name = artist

            # 搜索指定艺术家的子目录，并优先使用
            for artist_folder in os.listdir(ARTIST_BASE_PATH_FOR_DOCKER):
                # 如果该路径不是文件夹，则跳过
                if not os.path.isdir(os.path.join(ARTIST_BASE_PATH_FOR_DOCKER, artist_folder)):
                    continue

                keyword_pos = artist_folder.find(artist)
                if keyword_pos >= 0:
                    subdir_name = artist_folder
                    break

            # 创建子目录（如果不存在）
            subdir_path = os.path.join(
                ARTIST_BASE_PATH_FOR_DOCKER, subdir_name)
            os.makedirs(subdir_path, exist_ok=True)

            new_download_path = os.path.join(
                ARTIST_BASE_PATH_FOR_QB, subdir_name)

            print("Change subfolder of: ", name,
                  " to: ", new_download_path)

            # 修改种子下载路径
            client.set_torrent_location(torrent["hash"], new_download_path)
