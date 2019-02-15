# 资源版块
# i love nuonuo
# auther:KRzhao

import os
from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect, send_from_directory
from ..models import db, Resource
from ..decorators import staff_required

resource = Blueprint('resource', __name__, url_prefix='/resource/')


@resource.route('/')
@staff_required
def index():
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = Resource.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('resource/index.html', pagination=pagination)


@resource.route('/download/<int:resource_id>')
@staff_required
def download(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    directory = os.path.join(os.getcwd(), 'sphlps', 'static', 'resource')
    return send_from_directory(directory, resource.filename, as_attachment=True)
