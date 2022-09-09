from django.conf import settings
from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, PageNotAnInteger

from blog.models import Category, Article


def global_setting(request):
    """
    将settings里面的变量 注册为全局变量
    :param request:
    :return:
    """
    active_categories = Category.objects.filter(active=True).order_by('index')
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESCRIPTION,
        'SITE_KEY': settings.SECRET_KEY,
        'SITE_MAIL': settings.SITE_MAIL,
        'SITE_ICP': settings.SITE_ICP,
        'SITE_ICP_URL': settings.SITE_ICP_URL,
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_TYPE_CHINESE': settings.SITE_TYPE_CHINESE,
        'SITE_TYPE_ENGLISH': settings.SITE_TYPE_ENGLISH,
        'active_categories': active_categories
    }


class Index(View):
    """
    首页展示
     """

    def get(self, request):
        all_articles = Article.objects.all().order_by('-add_time')
        top_articles = Article.objects.filter(is_recommend=1)
        # 首页分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 9, request=request)
        articles = p.page(page)

        return render(request, 'index.html', {
            'all_articles': articles,
            'top_articles': top_articles,
        })
