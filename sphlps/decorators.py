# 存放特定角色的装饰器
# i love nuonuo
# author:KRzhao

from flask import abort
from flask_login import current_user
from functools import wraps
from .models import User


def role_required(role):
    """ 带参数的装饰器, 可以使用它保护一个路由处理函数只能被特定角色的用户访问:
    @role_required(User.Admin)
    def admin:
        pass
    """
    def decorator(func):
        @wraps(func)
        def warpper(*args, **kwargs):
            # 未登陆用户或者权限不足引发 404
            # 因为不想吧路由暴露给不具有权限的用户
            if not current_user.is_authenticated or current_user.role < role:
                abort(404)
            return func(*args, **kwargs)
        return warpper
    return decorator


# 特定角色的装饰器
user_required = role_required(User.ROLE_USER)
staff_required = role_required(User.ROLE_STAFF)
admin_required = role_required(User.ROLE_ADMIN)
master_required = role_required(User.ROLE_MASTER)
