# 客户版块: 资料/档案 等页面
# i love nuonuo
# auther:KRzhao

import os
from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect
from ..models import db, Customer, CustomerFile
from ..forms import CustomerFileForm
from ..decorators import admin_required

customer = Blueprint('customer', __name__, url_prefix='/customer/')


@customer.route('/')
@admin_required
def index():
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = Customer.query.paginate(
        page=page,
        per_page=current_app.config['CUSTOMER_PER_PAGE'],
        error_out=False
    )
    return render_template('customer/index.html', pagination=pagination)


@customer.route('/<int:customer_id>', methods=['GET', 'POST'])
@admin_required
def detail(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = CustomerFileForm()
    if form.validate_on_submit():
        directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'customer')
        filename = customer.name + '_' + form.type.data + '.' + form.file.data.filename.split('.')[-1]
        form.file.data.save(os.path.join(directory, filename))
        form.create_customer_file(customer_id, filename)
        flash('文件新增成功', 'success')
        return redirect(url_for('customer.detail', customer_id=customer.id))
    return render_template('customer/detail.html', customer=customer, files=customer.files, form=form)


@customer.route('customer_file/<filename>', methods=['GET', 'POST'])
@admin_required
def customer_file(filename):
    filename = 'customer' + '/' + filename
    return redirect(url_for('static', filename=filename))


@customer.route('edit_customer_file/<int:customer_file_id>', methods=['GET', 'POST'])
@admin_required
def edit_customer_file(customer_file_id):
    customer_file = CustomerFile.query.get_or_404(customer_file_id)
    customer = customer_file.customer
    form = CustomerFileForm(obj=customer_file)
    if form.validate_on_submit():
        directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'customer')
        # 删除旧文件
        os.remove(os.path.join(directory, customer_file.filename))
        filename = customer.name + '_' + form.type.data + '.' + form.file.data.filename.split('.')[-1]
        form.file.data.save(os.path.join(directory, filename))
        form.update_customer_file(customer_file, filename)
        flash('文件修改成功', 'success')
        return redirect(url_for('customer.detail', customer_id=customer.id))
    return render_template('customer/edit_customer_file.html', form=form, customer_file=customer_file)


@customer.route('delete_customer_file/<int:customer_file_id>', methods=['GET', 'POST'])
@admin_required
def delete_customer_file(customer_file_id):
    customer_file = CustomerFile.query.get_or_404(customer_file_id)
    customer = customer_file.customer
    directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'customer')
    os.remove(os.path.join(directory, customer_file.filename))
    db.session.delete(customer_file)
    db.session.commit()
    flash('文件"{}"删除成功! '.format(customer_file.filename), 'success')
    return redirect(url_for('customer.detail', customer_id=customer.id))
