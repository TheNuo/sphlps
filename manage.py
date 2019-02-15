# 主控模块
# i love nuonuo
# author:KRzhao

from .sphlps.app import create_app

# 使用开发环境配置
app = create_app('production')

if __name__ == '__main__':
    app.run()
