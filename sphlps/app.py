# Flask App 配置, 创建相关
# i love nuonuo
# author:KRzhao

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import configs
from .models import db, User


def create_app(config):
    """ App 工厂可以根据传入的 config 名称, 加载不同的配置 """
    app = Flask(__name__)
    # 加载配置文件到 app
    app.config.from_object(configs.get(config))
    # 将扩展注册到 app
    register_extensions(app)
    # 将蓝图注册到 app
    register_blueprints(app)
    return app


def register_extensions(app):
    """ 实现将 flask 的扩展注册到 app 的函数 """
    # SQLAlchemy 的初始化方式改为使用 init_app
    db.init_app(app)
    # 将 flask_migrate 注册到 app上
    Migrate(app, db)

    # 实例化 LoginManager 并使用 init_app 方法初始化 app
    login_manage = LoginManager()
    login_manage.init_app(app)

    @login_manage.user_loader
    def user_loader(id):
        """ 使用 user_loader 装饰器注册一个函数，用来告诉 flask-login 如何加载用户
        对象 """
        return User.query.get(id)
    # login_view 设置登录页面的路由，当用 flask-login 提供的 login_required 装饰器
    # 保护一个路由时，如果用户未登录，就会被重定向到 login_view 指定的页面。
    login_manage.login_view = 'front.login'


def register_blueprints(app):
    """ 实现将蓝图注册到 app 的函数 """
    from .handlers import front, admin, news, resource, customer
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(news)
    app.register_blueprint(resource)
    app.register_blueprint(customer)
