# - * -coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from myblog.models import ArticleModel, TopArticleModel, CommentModel, PostStarModel, \
                        BoardModel, CategoryModel, TagModel

class ArticleModelHelper(object):

    class ArticleSortType(object):
        '''
            sort_type：1 - 代表是按时间排序,
            sort_type：2 - 代表是按加精排序,
            sort_type：3 - 代表是按点赞量排序,
            sort_type：4 - 代表是按评论量排序,
        '''
        CREATE_TIME = 1
        HIGHLIGH_TIME = 2
        STAR_COUNT = 3
        COMMENT_COUNT = 4

        article_model = ArticleModel.objects.all()

    @classmethod
    # def post_list(cls, page, sort, board_id):
    def post_list(cls, page, sort):
        if sort == cls.ArticleSortType.CREATE_TIME:
            articles = article_model.order_by(ArticleModel.create_time.desc())
        elif sort == cls.ArticleSortType.HIGHLIGH_TIME:
            articles = article_model.order_by(
                TopArticleModel.create_time.desc(), ArticleModel.create_time.desc())
        elif sort == cls.ArticleSortType.STAR_COUNT:
            articles = article_model.query(ArticleModel).group_by(ArticleModel.id).order_by(
                db.func.count(ArticleStarModel.id).desc(), ArticleModel.create_time.desc())
        # 使用count这种方法需要从db导入func方法
        elif sort == cls.ArticleSortType.COMMENT_COUNT:
            articles = article_model.query(ArticleModel).group_by(ArticleModel.id).order_by(
                db.func.count(CommentModel.id).desc(), ArticleModel.create_time.desc())
        else:
            articles = ArticleModel.query.order_by(ArticleModel.create_time.desc())
        start = (page - 1) * constants.PAGE_NUM
        end = start + settings.PAGE_NUM

        articles = articles.filter(ArticleModel.is_removed == False)

        # 如果版块选项不为0，就根据版块id选择，如果为0就是全部，不需要筛选
        # if board_id:
        #     articles = articles.filter(ArticleModel.board_id == board_id)

        total_post = articles.count()
        total_page = total_post / constants.PAGE_NUM
        if total_post % constants.PAGE_NUM > 0:
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
            'articles': articles.slice(start, end),
            # 'boards': BoardModel.query.all(),
            'pages': pages,
            'c_page': page,
            't_page': total_page,
            'c_sort': sort,
            'c_board': board_id,
        }
        return context
