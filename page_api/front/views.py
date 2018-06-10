# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from frontauth import configs
from frontauth.decorators import front_login_required
from frontauth.utils import login,logout
from forms import FrontLoginForm,FrontRegistForm,ForgetpwdForm,\
        ResetEmailForm,ResetpwdForm,AddCommentForm,ReplyCommentForm,\
        AddArticleForm,SettingsForm
from frontauth.models import FrontUserModel

from page_api.common.basemodels import ArticleModelHelper
# from common.basemodel import ArticleModelHelper
from myblog.models import ArticleModel,CategoryModel,TagModel,TopModel,\
                CommentModel,ArticleStarModel
# from common.views import qiniu_token as front_qiniu_token
 


from utils import myjson, myemail
from utils.myemail import send_email


# 个人设置

def front_index(request):
    return render(request, 'front_index.html')

def front_login(request):
    if request.method == 'GET':
        return render(request,'front_login.html')
    else:
        form = FrontLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')

            user = login(request,email,password)
            if user and user.check_password(password):
                # request.session[configs.LOGINED_KEY] = str(user.uid)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                # 跳转到
                nexturl = request.GET.get('next')
                if nexturl:
                    return redirect(nexturl)
                else:
                    return redirect(reverse('front_index'))
            else:
                return render(request,'front_login.html',{"error":u'用户名和密码错误'})
        else:
            return render(request,'front_login.html',{'error':form.get_error()})


def front_regist(request):
    if request.method == 'GET':
        return render(request,'front_regist.html')
    else:
        form = FrontLoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            user = FrontRegistForm(telephone=telephone)
            user.save()
            return redirect(reverse('front_index')) 
        else:
            return render(request, 'front_regist.html', {'error':form.get_error()})


@front_login_required
def front_logout(request):
    logout(request)
    return redirect(reverse('front_index'))


# 修改邮箱
@front_login_required
def front_reset_email(request):
    if request.method == 'GET':
        return render(request, 'front_reset_email.html')
    else:
        # 如果邮箱在数据库存在，则无需修改
        # 否则才允许修改新密码
        form = ResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email', None)
            user = request.user
            if email:
                if request.email == email:
                    return myjson.json_params_error(u'新邮箱与老邮箱一致，无需修改！')
                else:
                    if send_mail(receivers=email):
                        user.email = email
                        user.save(update_fields=['email'])
                        return myjson.json_result(u'该邮箱验证成功！')
                    else:
                        return myjson.json_server_error()
            else:
                return myjson.json_params_error(message=u'必须输入邮箱！')
        else:
            return render(request, 'front_reset_email.html', {'error':form.get_error()})


# 个人主页
def front_profile(request):
    return render(request, 'front_profile.html')


# 设置
@front_login_required
def front_settings(request):
    if request.method == 'GET':
        return render(request, 'front_settings.html')
    else:
        form = SettingsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', None)
            realname = form.cleaned_data.get('realname', None)
            qq = form.cleaned_data.get('qq', None)
            avatar = form.cleaned_data.get('avatar', None)
            signature = form.cleaned_data.get('signature', None)
            gender = form.cleaned_data.get('gender', None)
            # 用户登录之后只要获取当前用户的信息，然后就可以直接传入数据
            user_model = request.user
            # 只有用户名是必填项，其他如果没有可以不填，所以需要判断,而性别是有默认选项
            user_model.username = username
            user_model.gender = gender
            if realname:
                user_model.realname = realname
            if qq:
                user_model.qq = qq
            if avatar:
                user_model.avatar = avatar
            if signature:
                user_model.signature = signature
            user_model.save()
            return myjson.json_result()
        else:
            return render(request, 'cms_reset_email.html', {'error':form.get_error()})

# 重置密码
@front_login_required
def front_reset_pwd(request):
    if request.method == 'GET':
        return render(request, 'front_reset_pwd.html')
    else:
        username = request.user
        form = ResetpwdForm(request.POST,user=username)
        if form.is_vaild():
            oldpwd = form.cleaned_data.get('oldpwd')
            newpwd = form.cleaned_data.get('newpwd')
            user = FrontUserModel.objects.filter(username=username,password=oldpwd).first()
            if user:
                is_vaild = user.check_password()
                if is_vaild:
                    user.set_password(newpwd)
                    user.save()
                    return myjson.json_result()
                else:
                    return myjson.json_params_error(message=u'密码验证错误！')
            else:
                user = user.create(username=username,password=newpwd)
                return myjson.json_result()
        else:
           return render(request, 'front_reset_pwd.html', {'error':form.get_error()})

# 忘记密码
@front_login_required
def front_forget_pwd(request):
    if request.method == 'GET':
        return render(request,'front_forget_pwd.html')
    else:
        form = ForgetpwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # request,email,check_url,cache_data=None,subject=None,message
            user = FrontUserModel.objects.filter(email=email).first()
            if user:
                if send_email(request,email,'front_reset_password'):
                    return HttpResponse(u'邮件发送成功')
                else:
                    return HttpResponse(u'邮件发送失败')
            else:
                return HttpResponse(u'该邮件不存在')
        else:
            return render(request,'front_forget_pwd.html',{'error':form.get_error()})



'''## 文章相关操作
1.前端和后台不一样，前端可以通过获取url的方式获取id，
但后端不允许，没有类似flask.request.form.get的方法，
因此后台通过Form的方式，前台通过urls.py修改url路由。

2.前台的删除方式和后台有别：
    2.1 后台删除是真正的从数据库删除
    2.2 前端删除只是在数据库给一个is_removed的字段，
        如果为True则说明被移除，False说明未删除，
        通过查询的时候过滤获取所有未删除的文章/评论等
'''

# 文章列表
def front_article_list(request,page=1,sort=1,category_id=0):
    context = ArticleModelHelper.article_list(page, sort, category_id)
    return render(request, 'front_article_list.html',context=context)

# 文章详情页
def front_article_detail(request, article_id):
    '''我们需要获取的有：
       1. 文章(ArticleModel)
       2. 标签(TagModel)
       3. 分类(CategoryModel)
       4. 评论(CommentModel)
       5. 点赞(ArticleStarModel)
       另外，阅读量访问一次+1，还需获取当前的分类
    '''
    article_model = ArticleModel.objects.filter(pk=article_id,is_removed=False)
    if article_model:
        # 每次访问阅读量都+1
        article_model.read_count += 1
        article_model.save()
        # 获取所有给这篇文章点赞的作者
        star_author_ids = [star_model.author.id for star_model in article_model.stars]
        context = {
            'articles':article_model,
            'comments': article_model.commentmodel_set.all(),
            'tags': TagModel.objects.all(),
            'categorys': CategoryModel.objects.all(),
            # 当前文章分类
            'c_category': article_model.category,
            # 当前文章分类
            'c_tag': article_model.tags,
            'star_author_ids': star_author_ids
        }
        return render(request, 'front_article_detail.html', context=context)
    else:
        return myjson.json_params_error(u'该文章不存在！')

# 添加文章
@front_login_required
def front_add_article(request):
    # 添加文章
    # 1.请求页面时，我们需要获取所有的标签和分类
    # 2.提交修改后的页面时，检查分类和标签在数据库中是否存在，
    # 如果不存在则新建，否则存入
    # 3.文章与标签是多对多关系，与其他内容不一起存
    # 4.文章与分类不是是多对多关系
    if request.method == 'GET':
        tags = TagModel.objects.all()
        categorys = CategoryModel.objects.all()
        context = {
            'tags':tags,
            'categorys':categorys
        }
        return render(request, 'front_add_article.html', context=context)
    else:
        form = AddArticleForm(request.POST)
        if form.is_valid():
            user = request.user
            tag_ids = request.POST.getlist('tags[]')

            title = form.cleaned_data.get('title')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')

            category = CategoryModel.objects.filter(pk=category_id).first()

            article_model = ArticleModel(
                username=user,
                title=title,
                thumbnail=thumbnail,
                content=content,
                category=category
                )
            article_model.save()
            # 文章与标签的多对多的保存
            # 如果选择了标签，则将选择的标签以此存入，否则不用存
            if tag_ids:
                for tag_id in tag_ids:
                    tag_model = TagModel.objects.filter(pk=tag_id).first()
                    if tag_model:
                        article_model.tags.add(tag_model)
            return myjson.json_result()
        else:
            return render(request, 'front_add_article.html', {'error':form.get_error()})

# 编辑文章
@front_login_required
def front_edit_article(request):
    '''
       它的逻辑和add_article相似，但作者不会变，只需获取文章的id
       我们会用到一篇已存在的article里的的所有数据，包括tags
       但文章里的tags会通过article.tags多对多的方式获取，而不再从tagmodel获取
       因为可能会修改tags，我们仍需要传入所有的tags
       因此我们需要将tags添加到article里，而为了方便使用，也为了添加tags
       我们会使用到model_to_dict这个函数，将数据库里的数据提取出来并转化成dict类型
    '''
    if request.method == 'GET':
        article_id = request.GET.get('article_id', None)
        if article_id:
            article_model = ArticleModel.objects.filter(pk=article_id).first()
            article_dict = model_to_dict(article_model)
            tag_model = article_model.tags.all()
            article_dict['tags'] = [tag_model.id for tags in tag_model]
            context = {
                'categorys': CategoryModel.objects.all(),
                'tags': TagModel.objects.all(),
                'article': article_dict
            }
            return render(request, 'front_add_article.html', context=context)
        else:
            return myjson.json_params_error(u'没有该id！')
    else:
        form = EditArticleForm(request.POST)
        if form.is_valid():
            tag_ids = request.POST.getlist('tags[]')

            article_id = form.cleaned_data.get('article_id')
            title = form.cleaned_data.get('title')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')

            article_model = ArticleModel.objects.filter(pk=article_id).first()
            category = CategoryModel.objects.filter(pk=category_id).first()

            # 修改和创建的方式不一样
            if article_model:
                article_model.title = title
                article_model.thumbnail = thumbnail
                article_model.content = content
                article_model.category = category
                article_model.save()

            # 文章与标签的多对多的保存
            # 如果选择了标签，则将选择的标签以此存入，否则不用存
            if tag_ids:
                for tag_id in tag_ids:
                    tag_model = TagModel.objects.filter(pk=tag_id).first()
                    if tag_model:
                        article_model.tags.add(tag_model)
            return myjson.json_result()
        else:
            return render(request, 'front_edit_article.html', {'error':form.get_error()})


# 删除文章，和后端不同，前台只删除，但不真正删除
@front_login_required
def front_delete_article(request):
    article_id = request.GET.get('article_id', None)
    if article_id:
        article_model = ArticleModel.objects.filter(article_id=article_id).first()
        if article_model:
            article_model.is_removed = True
            article_model.save()
            return redirect(reverse('article_list'))
        else:
            return myjson.json_params_error(u'该文章不存在！')
    else:
        return myjson.json_params_error(u'没有该id！')


# 文章点赞
@front_login_required
@require_http_methods(['POST'])
def front_article_star(request):
    '''点赞和取消点赞，同置顶
        1. 如果文章已点赞则无需再点赞，未点赞则点赞。
        2. 如果选择的是点赞（不点赞），而数据库中存的也是点赞（不点赞），
            则不需操作，抛出异常
            如果选择的是点赞，而数据库中存的是不点赞，则删除该字段
            如果选择的是不点赞，而数据库中存的是点赞，则创建改字段
        3. 修改TopModel之后也要更改ArticleModel的top字段
    '''
    form = ArticleStarForm(request.POST)
    if form.is_valid():
        article_id = form.cleaned_data.get('article_id')
        # 本文章选择的是置顶还是不置顶
        is_star = form.cleaned_data.get('is_star')
        article_model = ArticleModel.objects.filter(pk=article_id).first()
        star_model = ArticleStarModel.objects.filter(pk=article_id).first()
        if article_model:
            if is_star:
                if star_model:
                    return myjson.json_params_error(message=u'该文章已经置顶！')
                else:
                    star_model = ArticleStarModel()
                    star_model.author = request.user.username
                    star_model.article = article_model
                    star_model.save()
                    return myjson.json_result()
            else:
                if star_model:
                    star_model.delete()
                    return myjson.json_result()
                else:
                    return myjson.json_params_error(message=u'该文章没有置顶！')
    else:
        return myjson.json_params_error(message=form.get_error())

# 评论列表
def front_comment_list(request, page=1):
    context = ArticleModelHelper.common_page(page=page, model_name=CommentModel,key_name='comments')
    return render(request, 'front_comment_list.html',context=context)

# 增加评论
@front_login_required
def front_add_comment(request):
    if request.method == 'GET':
        article_id = request.GET.get('article_id')
        context = {
            'articles':ArticleModel.objects.filter('article_id').first()
        }
        return render(request,'front_add_article.html',context=context)
    else:
        form = AddCommentForm(request.POST)
        if form.is_valid():
            article_id = form.cleaned_data.get('article_id')
            comment = form.cleaned_data.get('comment')
            comment_model = CommentModel(comment=comment)
            article_model = ArticleModel.objects.filter('article_id').first()
            comment_model.article = article_model
            comment_model.author = request.user.username
            comment_model.save()
            return myjson.json_result()
        else:
            return render(request,'front_add_article.html',{'errors':form.error})

# 删除评论
@front_login_required
@require_http_methods(['POST'])
def front_delete_comment(request):
    comment_id = request.GET.get('comment_id', None)
    if comment_id:
        comment_model = CommentModel.objects.filter(pk=comment_id).first()
        if comment_model:
            comment_model.is_removed = True
            comment_model.save()
            return myjson.json_result()
        else:
            return myjson.json_params_error(message=u'该评论不存在！')
    else:
        return myjson.json_params_error(u'没有该id！')

# 回复评论
@front_login_required
def front_reply_comment(request):
    '''回复评论需要：文章id，被回复的评论id（即原始评论），回复内容
    '''
    if request.method == 'GET':
        article_id = request.GET.get('article_id', None)
        comment_id = request.GET.get('comment_id', None)
        if article_id:
            article_model = ArticleModel.objects.filter(pk=article_id).first()
            if article_model:
                context = {
                    'articles':article_model
                }
                if comment_id:
                    # 原始评论
                    origin_comment = CommentModel.objects.filter(pk=comment_id).first()
                    if origin_comment:
                        context['origin_comment'] = origin_comment
        return render(request,'front_add_article.html', context)
    else:
        form = ReplyCommentForm(request.POST)
        if form.is_valid():
            article_id = form.cleaned_data.get('article_id',None)
            comment_id = form.cleaned_data.get('comment_id',None)
            content = form.cleaned_data.get('content',None)
            if article_id:
                article_model = ArticleModel.objects.filter(article_id).first()
                if content:
                    comment_model = CommentModel(content=content)
                    comment_model.article = article_model
                    comment_model.author = request.user.username
                    if comment_id:
                        origin_comment = CommentModel.objects.filter(pk=comment_id).first()
                        comment_model.origin_comment = origin_comment
                        comment_model.save()
                    return myjson.json_result()
                else:
                    return myjson.json_params_error(u'没有评论内容！')
            else:
                return myjson.json_params_error(u'没有该评论！')
        else:
            return myjson.json_params_error(message=form.errors)

# 查找
def front_search(request):
    q = request.GET.GET('query')
    if q:
        # 查询条件忽略大小写
        article_model = ArticleModel.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context = {
            'articles':article_model,
            'categorys': CategoryModel.objects.all()
        }
        # return myjson.json_result()
        return render(request,'front_search.html',context=context)
    else:
        return myjson.json_params_error(message=u'请输入查询字符串')