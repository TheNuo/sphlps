# 客户版块: 资料/档案 等页面
# i love nuonuo
# auther:KRzhao

from flask import Blueprint, render_template, url_for, request, current_app
from ..models import News

news = Blueprint('news', __name__, url_prefix='/news/')


@news.route('/')
def index():
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = News.query.paginate(
        page=page,
        per_page=current_app.config['NEWS_PER_PAGE'],
        error_out=False
    )
    return render_template('news/index.html', pagination=pagination)


@news.route('/<int:news_id>')
def detail(news_id):
    news = News.query.get_or_404(news_id)
    # 判断是否存在图片, 拼接存放目录和文件名
    if news.image:
        news.image = 'news/' + news.image
    return render_template('news/detail.html', news=news)
