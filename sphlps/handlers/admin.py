# 管理板块: 管理后台
# i love nuonuo
# auther:KRzhao

import os
from flask import Blueprint, render_template, url_for, redirect, flash, abort, request, current_app
from ..models import News, Resource, Customer
from ..forms import db, User, RoleEditForm, NewsForm, ResourceForm, CustomerForm
from ..decorators import admin_required

admin = Blueprint('admin', __name__, url_prefix='/admin/')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/user')
@admin_required
def user():
    """ pagination 方法主要接受 3 个参数,
    page: 第几页
    per_page: 每页显示数目
    error_out: 如果设置为 True，那么发生错误时会引发 404；如果设置为 False，发生错误时返回的是第 1 页的 Pagination 对象
    """
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/user.html', pagination=pagination)


@admin.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.username in ['赵家华', '余诺']:
        abort(404)
    else:
        form = RoleEditForm(obj=user)
        if form.validate_on_submit():
            form.update_user(user)
            flash('用户信息修改成功', 'success')
            return redirect(url_for('admin.user'))
        return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/user/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.username in ['赵家华', '余诺']:
        abort(404)
    else:
        db.session.delete(user)
        db.session.commit()
        flash('用户"{}"删除成功! '.format(user.username), 'success')
        return redirect(url_for('admin.user'))


@admin.route('/news')
@admin_required
def news():
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = News.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/news.html', pagination=pagination)


@admin.route('/news/create', methods=['GET', 'POST'])
@admin_required
def create_news():
    form = NewsForm()
    if form.validate_on_submit():
        # 判断表单中是否上传了图片文件
        if form.image.data:
            # 使用 os.path.join 拼接储存目录
            directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'news')
            image = form.name.data + '.' + form.image.data.filename.split('.')[-1]
            # 储存文件到本地
            form.image.data.save(os.path.join(directory, image))
        else:
            image = None
        form.create_news(image)
        flash('新闻创建成功', 'success')
        return redirect(url_for('admin.news'))
    return render_template('admin/create_news.html', form=form)


@admin.route('/news/<int:news_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_news(news_id):
    news = News.query.get_or_404(news_id)
    form = NewsForm(obj=news)
    if form.validate_on_submit():
        if form.image.data:
            directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'news')
            image = form.name.data + '.' + form.image.data.filename.split('.')[-1]
            form.image.data.save(os.path.join(directory, image))
        else:
            image = news.image
        form.update_news(news, image)
        flash('新闻修改成功', 'success')
        return redirect(url_for('admin.news'))
    return render_template('admin/edit_news.html', form=form, news=news)


@admin.route('/news/<int:news_id>/delete')
@admin_required
def delete_news(news_id):
    news = News.query.get_or_404(news_id)
    if news.image:
        directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'news')
        os.remove(os.path.join(directory, news.image))
    db.session.delete(news)
    db.session.commit()
    flash('新闻"{}"删除成功! '.format(news.name), 'success')
    return redirect(url_for('admin.news'))


@admin.route('/resource')
@admin_required
def resource():
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = Resource.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/resource.html', pagination=pagination)


@admin.route('/resource/create', methods=['GET', 'POST'])
@admin_required
def create_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        # 使用 os.path.join 拼接储存目录
        directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'resource')
        filename = form.type.data + '_' + form.name.data + '.' + form.file.data.filename.split('.')[-1]
        form.file.data.save(os.path.join(directory, filename))
        # 判断表单中是否上传了图片文件
        if form.image.data:
            image = form.type.data + '_' + form.name.data + '.' + form.image.data.filename.split('.')[-1]
            form.image.data.save(os.path.join(directory, image))
        else:
            image = None
        form.create_resource(filename, image)
        flash('文件上传成功', 'success')
        return redirect(url_for('admin.resource'))
    return render_template('admin/create_resource.html', form=form)


@admin.route('/resource/<int:resource_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    form = ResourceForm(obj=resource)
    if form.validate_on_submit():
        if form.image.data:
            directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'resource')
            image = form.type.data + '_' + form.name.data + '.' + form.image.data.filename.split('.')[-1]
            form.image.data.save(os.path.join(directory, image))
        else:
            image = resource.image
        form.update_resource(resource, image)
        flash('文件修改成功', 'success')
        return redirect(url_for('admin.resource'))
    return render_template('admin/edit_resource.html', form=form, resource=resource)


@admin.route('/resource/<int:resource_id>/delete')
@admin_required
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'resource')
    if resource.image:
        os.remove(os.path.join(directory, resource.image))
    os.remove(os.path.join(directory, resource.filename))
    db.session.delete(resource)
    db.session.commit()
    flash('文件"{}"删除成功! '.format(resource.name), 'success')
    return redirect(url_for('admin.resource'))


@admin.route('/customer')
@admin_required
def customer():
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = Customer.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/customer.html', pagination=pagination)


@admin.route('/customer/create', methods=['GET', 'POST'])
@admin_required
def create_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        form.create_customer()
        flash('客户创建成功', 'success')
        return redirect(url_for('admin.customer'))
    return render_template('admin/create_customer.html', form=form)


@admin.route('/customer/<int:customer_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        form.update_customer(customer)
        flash('客户信息修改成功', 'success')
        return redirect(url_for('admin.customer'))
    return render_template('admin/edit_customer.html', form=form, customer=customer)


@admin.route('/customer/<int:customer_id>/delete')
@admin_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash('客户"{}"删除成功! '.format(customer.name), 'success')
    return redirect(url_for('admin.customer'))

