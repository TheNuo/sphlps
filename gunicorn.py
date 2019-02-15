# Gunicorn 配置文件, 使用 gunicorn -c gunicorn.py manage:app 启动 web 应用

import multiprocessing

bind = '0.0.0.0:80'

workers = multiprocessing.cpu_count() * 2 + 1
