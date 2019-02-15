# 存放数据模型相关代码
# i love nuonuo
# author:KRzhao

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# 注意这里不再传入 app 了
db = SQLAlchemy()


class Base(db.Model):
    """ 所有 model 的一个基类， 默认添加了时间戳 """
    # 不将这个类当作 Model 类
    __abstract__ = True
    # 设置了 default 和 onupdate，这两个时间戳不需要手动维护
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)


class User(Base, UserMixin):
    """ 用户数据模型, 使用 flask_login 的 UserMixin 提供 session 管理功能, 实现用户
    的登录 登出 记住用户等功能 """
    __tablename__ = 'user'

    # 用数值表示角色, 用于判断是否有权限
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30
    ROLE_MASTER = 777

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, index=True, nullable=False)
    email = db.Column(db.String(32), unique=True, index=True, nullable=False)
    # sqlalchemy 会以属性名来定义数据表字段名, 这里需要使用私有属性, 所以明确指定数据表字段名
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        """ 显示一个可读字符串, 方便调试 """
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        """ Python 风格的 getter """
        return self._password

    @password.setter
    def password(self, orig_password):
        """ Python 风格的 setter, 设置 user.password 时,
        自动将 password 生成哈希值再存入数据数据表 """
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """ 判断输入的密码和数据表储存的密码是否相等 """
        return check_password_hash(self._password, password)

    @property
    def is_staff(self):
        return self.role >= self.ROLE_STAFF

    @property
    def is_admin(self):
        return self.role >= self.ROLE_ADMIN

    @property
    def is_master(self):
        return self.role == self.ROLE_MASTER


class News(Base):
    """ 文章数据模型 """
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    # 储存文章的分类信息
    type = db.Column(db.String(16), nullable=False)
    description = db.Column(db.String(256))
    content = db.Column(db.Text)
    # 储存文章插图的文件名
    image = db.Column(db.Integer)

    def __repr__(self):
        """ 显示一个可读字符串, 方便调试 """
        return '<News:{}>'.format(self.name)


class Resource(Base):
    """ 资源库数据模型 """
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    type = db.Column(db.String(16), index=True, nullable=False)
    image = db.Column(db.String(32))
    filename = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        """ 显示一个可读字符串, 方便调试 """
        return '<Resource:{}>'.format(self.name)


class Customer(Base):
    """ 客户数据模型 """
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, index=True, nullable=False)
    code = db.Column(db.String(32), unique=True, index=True, nullable=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    nature = db.Column(db.String(32), nullable=False)
    archives = db.Column(db.String(32), unique=True)
    area = db.Column(db.String(32))
    contacts = db.Column(db.String(32))
    phone_number = db.Column(db.String(32))
    files = db.relationship('CustomerFile')

    def __repr__(self):
        """ 显示一个可读字符串, 方便调试 """
        return '<Customer:{}>'.format(self.name)


class CustomerFile(Base):
    """ 客户文件数据模型 """
    __tablename__ = 'customer_file'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), nullable=False)
    filename = db.Column(db.String(32), nullable=False)
    # 外键的 ondelete='CASCADE', 需要在 relationship 中的 backref 参数设置 cascade='all, delete-orphan' 才能实现级联删除
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'))
    customer = db.relationship('Customer',
                               backref=db.backref('customer_file', cascade='all, delete-orphan'))

    def __repr__(self):
        """ 显示一个可读字符串, 方便调试 """
        return '<Customer_file:{} - {}>'.format(self.customer.name, self.type)
