# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^$', views.cms_article_list, name="cms_index"),
    url(r'^login/$', views.cms_login, name="cms_login"),
    url(r'^logout/$',views.cms_logout,name='cms_logout'),
    url(r'^reset_email/$',views.cms_reset_email,name='cms_reset_email'),
    url(r'^reset_pwd/$',views.cms_reset_pwd,name='cms_reset_pwd'),
    url(r'^cms_profile/$',views.cms_profile,name='cms_profile'),
    url(r'^settings/$',views.cms_settings,name='cms_settings'),
    url(r'^article_list/$',views.cms_article_list,name='cms_article_list'),
    # url(r'^article_list/(?P<sort>\d+)/(?P<page>\d+)/(?P<category_id>\d+)/$',views.cms_article_list,name='cms_article_list'),
    url(r'^add_article/$',views.cms_add_article,name='cms_add_article'),
    url(r'^edit_article/$',views.cms_edit_article,name='cms_edit_article'),
    url(r'^delete_article/$',views.cms_delete_article,name='cms_delete_article'),
    url(r'^top_article/$',views.cms_top_article,name='cms_top_article'),
    # url(r'^get_token/$',views.get_token,name='cms_get_token'),
    # url(r'^check_email/(?P<code>\w+)$',views.check_email,name='cms_check_email'),
    url(r'^comment_list/$',views.cms_comment_list,name='cms_comment_list'),
    url(r'^remove_comment/(?P<comment_id>[\w\-]+)/$',views.cms_remove_comment,name='cms_remove_comment'),
    url(r'^category_list/$',views.cms_category_list,name='cms_category_list'),
    url(r'^add_category/$',views.cms_add_category,name='cms_add_category'),
    url(r'^edit_category/$',views.cms_edit_category,name='cms_edit_category'),
    url(r'^remove_category/$',views.cms_remove_category,name='cms_remove_category'),
    url(r'^tag_list/$',views.cms_tag_list,name='cms_tag_list'),
    url(r'^add_tag/$',views.cms_add_tag,name='cms_add_tag'),
    url(r'^remove_tag/$',views.cms_remove_tag,name='cms_remove_tag'),
    url(r'^test/$',views.test),
]
