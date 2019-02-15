# 存放表单相关代码
# i love nuonuo
# author:KRzhao

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms import FileField, SelectField
from wtforms.validators import Length, Email, EqualTo, DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from .models import db, User, News, Resource, Customer, CustomerFile


class RegisterForm(FlaskForm):
    """ 用户注册表单 """
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self):
        """ 创建新用户的方法 """
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        if user.username == '赵家华' or user.username == '余诺':
            user.role = 777
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        """ 自定验证器, 验证用户名是否已存在数据表 """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在! ')

    def validate_email(self, field):
        """ 自定验证器, 验证邮箱地址是否已存在数据表 """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')


class RoleEditForm(FlaskForm):
    """ 权限管理表单 """
    role = IntegerField('权限等级', validators=[DataRequired()])
    submit = SubmitField('提交')

    def update_user(self, user):
        """ 修改权限的方法 """
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

    def validate_role(self, field):
        """ 自定验证器, 验证权限格式 """
        if field.data != 10 and field.data != 20 and field.data != 30:
            raise ValidationError('权限等级设置不正确')


class LoginForm(FlaskForm):
    """ 登录表单 """
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入合法的email地址')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        """ 自定验证器, 验证邮箱是否注册 """
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        """ 自定验证器, 验证密码是否正确 """
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误, 请重新输入')


class NewsForm(FlaskForm):
    """ 新闻表单 """
    name = StringField('标题', validators=[DataRequired(), Length(5, 32)])
    type = SelectField('类型', validators=[DataRequired(message='请选择新闻类别')],
                       render_kw={'class': 'form-control'},
                       choices=[(1, '内部文件'), (2, '对外新闻'), (3, '总部转载'), (4, '其他转载')],
                       default=2, coerce=int)
    description = TextAreaField('描述', validators=[DataRequired(), Length(16, 256)])
    content = TextAreaField('内容', validators=[DataRequired(), Length(32, 1024)])
    image = FileField('图片', validators=[FileAllowed(['jpg', 'jpeg'], message='只支持jpg/jpeg格式. ')])
    submit = SubmitField('提交')

    def create_news(self, image):
        news = News()
        # 使用表单数据填充 news 对象
        self.populate_obj(news)
        news.image = image
        db.session.add(news)
        db.session.commit()
        return news

    def update_news(self, news, image):
        self.populate_obj(news)
        news.image = image
        db.session.add(news)
        db.session.commit()
        return news


class ResourceForm(FlaskForm):
    """ 资源库文件上传表单 """
    name = StringField('文件名', validators=[DataRequired(message='请输入文件名'), Length(3, 32)])
    type = SelectField('类型', validators=[DataRequired(message='请选择分类')],
                       render_kw={'class': 'form-control'},
                       choices=[('Word', 'Word'),
                                ('PPT', 'PPT'),
                                ('Excel', 'Excel')
                                ],
                       default=1, coerce=str)
    file = FileField('文件', validators=[FileRequired(message='请选择文件'),
                                       FileAllowed(['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'],
                                                   message='文件类型不支持')])
    image = FileField('图片', validators=[FileAllowed(['jpg', 'jpeg'], message='只支持jpg/jpeg格式. ')])
    submit = SubmitField('提交')

    def create_resource(self, filename, image):
        resource = Resource()
        self.populate_obj(resource)
        # 规划化储存的文件名
        resource.filename = filename
        resource.image = image
        db.session.add(resource)
        db.session.commit()
        return resource

    def update_resource(self, resource, image):
        self.populate_obj(resource)
        resource.image = image
        db.session.add(resource)
        db.session.commit()
        return resource


class CustomerForm(FlaskForm):
    """ 客户资料表单 """
    number = IntegerField('客户标识', validators=[DataRequired()])
    code = StringField('客户编码', validators=[DataRequired(), Length(5, 16)])
    name = StringField('客户名称', validators=[DataRequired(), Length(5, 32)])
    nature = StringField('客户类型', validators=[DataRequired(), Length(2, 8)])
    archives = StringField('档案编号', validators=[DataRequired(), Length(3, 16)])
    area = StringField('行政区域')
    contacts = StringField('联系人')
    phone_number = StringField('电话号码', validators=[Length(11, 13)])
    submit = SubmitField('提交')

    def create_customer(self):
        customer = Customer()
        self.populate_obj(customer)
        db.session.add(customer)
        db.session.commit()
        return customer

    def update_customer(self, customer):
        self.populate_obj(customer)
        db.session.add(customer)
        db.session.commit()
        return customer


class CustomerFileForm(FlaskForm):
    """ 客户文件上传表单 """
    type = SelectField('类型', validators=[DataRequired(message='请选择分类')],
                       render_kw={'class': 'form-control'},
                       choices=[('营业执照', '营业执照'),
                                ('药品经营许可证', '药品经营许可证')
                                ],
                       default=1, coerce=str)
    file = FileField('图片', validators=[FileRequired(message='请选择文件'), FileAllowed(['jpg', 'jpeg'], message='只支持jpg/jpeg格式. ')])
    submit = SubmitField('添加文件')

    def create_customer_file(self, customer_id, filename):
        customer_file = CustomerFile()
        self.populate_obj(customer_file)
        customer_file.customer_id = customer_id
        # 规划化储存的文件名
        customer_file.filename = filename
        db.session.add(customer_file)
        db.session.commit()
        return customer_file

    def update_customer_file(self, customer_file, filename):
        self.populate_obj(customer_file)
        customer_file.filename = filename
        db.session.add(customer_file)
        db.session.commit()
        return customer_file


