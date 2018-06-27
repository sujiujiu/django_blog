# - * -coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from myblog.models import ArticleModel, TopModel, CommentModel, \
                        CategoryModel, TagModel, ArticleStarModel

class ArticleModelHelper(object):

    class ArticleSortType(object):
        '''
            sort_type：1 - 代表是按时间排序,(默认)
            sort_type：2 - 代表是按置顶排序,
            sort_type：3 - 代表是按点赞量排序,
            sort_type：4 - 代表是按评论量排序,
        '''
        CREATE_TIME = 1
        TOP_RANK = 2
        STAR_COUNT = 3
        COMMENT_COUNT = 4

    @classmethod
    def common_page(cls, articles, total_articles, page, key_name):
        page_num = settings.PAGE_NUM
        start = (page - 1) * page_num
        end = start + page_num

        # total_articles = articles.count()
        total_page = total_articles / page_num
        if total_articles % page_num > 0:
            total_page += 1

        pages = []
        # 左边的判断
        left_page = page - 1
        while left_page >= 1:
            if left_page % 5 == 0:
                break
            pages.append(left_page)
            left_page -= 1

        # 右边的判断
        right_page = page
        while right_page <= total_page:
            if right_page % 5 == 0:
                pages.append(right_page)
                break
            else:
                pages.append(right_page)
                right_page += 1

        pages.sort()

        context = {
            '%s' % key_name : articles.values()[start:end],
            'pages': pages,
            'c_page': page,
            't_page': total_page
        }
        return context

    @classmethod
    def article_list(cls, sort, page, category_id):
        sort,category_id,page = int(sort),int(category_id),int(page)
        article_model = ArticleModel.objects.all()

        if sort == cls.ArticleSortType.TOP_RANK:
            articles = article_model.order_by(
                '-top__create_time',
                '-create_time')
        elif sort == cls.ArticleSortType.STAR_COUNT:
            articles = ArticleModel.objects.values('pk').annotate(
                star_counts=Count('articlestar__pk')).order_by(
                    '-star_counts','-create_time'
                )
        elif sort == cls.ArticleSortType.COMMENT_COUNT:
            articles = ArticleModel.objects.values('pk').annotate(
                comment_counts=Count('comment__pk')).order_by(
                    '-comment_counts','-create_time'
                )
        else:
            articles = article_model

        articles = articles.filter(is_removed=False)

        # 如果分类选项不为0，就根据分类id选择，如果为0就是全部，不需要筛选
        if category_id:
            articles = articles.filter(category=category_id)

        total_articles = articles.count()

        context = cls.common_page(
            articles=articles,
            total_articles=total_articles,
            page=page,
            key_name='articles'
        )
        
        context.update({
            'c_sort': sort,
            'c_category': category_id,
            'categorys': CategoryModel.objects.all()
        })
        return context
