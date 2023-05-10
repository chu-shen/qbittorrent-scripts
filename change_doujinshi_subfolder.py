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
        if any(word in download_path for word in SKIP_PATH):
            continue

        # 使用正则表达式匹配
        match = re.search(EVENT_REGEX, name)

        if match:
            event = match.group(0)

            # 检查路径是否已包含前缀子目录
            if not download_path.endswith(event):

                # 可以重新指定Event目录
                # download_path = download_path.replace("/QB/Doujinshi/E-Hentai", "/QB/Doujinshi/Event")
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
    # 获取子目录列表
    subdirs = [d for d in os.listdir(ARTIST_BASE_PATH_FOR_DOCKER) if os.path.isdir(
        os.path.join(ARTIST_BASE_PATH_FOR_DOCKER, d))]

    # 循环所有种子
    for torrent in torrents:
        # 获取种子下载路径
        download_path = torrent["save_path"]

        # 跳过指定路径
        if any(word in download_path for word in SKIP_PATH):
            continue

        # 获取种子名称
        name = torrent["name"]
        torrent_info=extract_torrent_info(name)
        if torrent_info is not None:
            name_parts = [part for part in torrent_info[1:3] if part is not None]
            name = ','.join(name_parts)

        # 获取目录下所有子目录
        for subdir in subdirs:
            group, artist = extract_dir_info(subdir)

            # 使用正则表达式匹配
            if group:
                pattern = r'{}|{}'.format(group, artist)
            else:
                pattern = r'{}'.format(artist)
            match = 0
            if re.search(pattern, name):
                match = 1

            if match:
                new_download_path = os.path.join(
                    ARTIST_BASE_PATH_FOR_QB, subdir)

                print("Change subfolder of: ", torrent["name"],
                      " to: ", new_download_path)

                # 修改种子下载路径
                client.set_torrent_location(torrent["hash"], new_download_path)




def extract_dir_info(name):
    """
    提取团体和艺术家信息

    Args:
        name: 艺术家名称

    Returns:
        团体和艺术家信息元组
    """
    # 定义正则表达式匹配规则
    pattern = r'^(.+?)\s*\((.+?)\)$'

    # 进行正则表达式匹配
    match = re.match(pattern, name)

    if match:
        # 如果匹配成功，则提取团体和艺术家信息
        group = match.group(1)
        artist = match.group(2)
    else:
        # 如果匹配失败，则整体视为艺术家
        group = ''
        artist = name

    return group, artist


def extract_torrent_info(name):
    """
    提取活动、团体和艺术家信息

    Args:
        name: 种子名称

    Returns:
        活动、团体和艺术家信息元组
    """
    # 定义正则表达式
    # pattern = r'^(?:\((.*?)\))?\s*\[(.*?)\s*(?:\((.*?)\))?]\s*(.*?)\s*(?:\((.*?)\))?\s*\[(.*?)\]'
    pattern = r'^(?:\((.*?)\))?\s*\[(.*?)\s*(?:\((.*?)\))?]\s*'

    # 匹配正则表达式
    match = re.match(pattern, name)

    # 如果匹配失败，则返回None
    if match is None:
        return None

    # 提取信息
    return match.groups()
