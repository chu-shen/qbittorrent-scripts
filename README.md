# qbittorrent-scripts

## 修改同人志子目录

将QB RSS订阅下载的同人志再次进行分类整理

### 配置

将 `config.template.py` 重命名为 `config.py` ，并修改如下配置:

- QB_URL：QB链接
- QB_USER：QB用户
- QB_PASSWORD：QB用户密码
- SKIP_PATH：需要跳过的QB路径

- EVENT_REGEX：需要创建子目录的Event。建议搭配QB RSS正则使用，将所有Event下载至Event目录，然后使用此脚本分类

- ARTIST_BASE_PATH_FOR_DOCKER：脚本运行环境（比如Docker）能访问到文件的艺术家目录。会根据此目录下艺术家名称在种子中查找。
- ARTIST_BASE_PATH_FOR_QB：QB保存文件时使用的艺术家目录



### 使用

```shell
pip install python-qbittorrent

python main.py
```

### TODO

- 调整Artist整理逻辑
    - 英文名匹配问题
    - 匹配不精准问题
- 调整Event整理逻辑
