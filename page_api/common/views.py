# -*- coding: utf-8 -*-
import top

from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.http import require_http_methods

from frontauth.decorators import front_login_required

from forms import ResetEmailForm,ResetpwdForm,\
                AddCategoryForm,AddTagForm,AddArticleForm,EditArticleForm,\
                CategoryForm,EditCategoryForm
from myblog.models import ArticleModel,CategoryModel,TagModel,TopModel,\
                CommentModel,ArticleStarModel


from utils.captcha.mycaptcha import Captcha
from utils.myemail import send_email
from utils import myjson
import qiniu

from PIL import Image
try:
	from cStringIO import StringIO
except ImportError:
	from io import BytesIO as StringIO

# 图形验证码
def graph_captcha(request):
	text,image = Captcha.gene_code()
	out = StringIO() 
	# 将StringIO的指针指向开始的位置
    out.seek(0)
    # 指定响应的类型
    response = HttpResponse(content_type='image/png')
    # 把图片流给读出来
    response.write(out.read())
    return response


# 短信验证码
def sms_captcha(request):
    telephone = request.GET.get('telephone')
    # 获取用户名，用于发送短信验证码显示用户名
    if not telephone:
        return myjson.json_params_error(message=u'必须指定手机号码！')
    if cache.get(telephone):
        return myjson.json_params_error(message=u'验证码已发送，请1分钟后重复发送！')
    # if not username:
    #     return myjson.json_params_error(message=u'必须输入用户名！')
    # 阿里大于APP_KEY及APP_SECRET
    app_key = settings.APP_KEY
    app_secret = settings.APP_SECRET
    request = top.setDefaultAppInfo(app_key, app_secret)
    request = toprequest.api.AlibabaAliqinFcSmsNumSendRequest()
    request.extend = ""
    request.sms_type = 'normal'
    # 签名名称
    request.sms_free_sign_name = settings.SIGN_NAME
    # 随即生成字符串
    captcha = Captcha.gene_text()
    # 设置短信的模板
    request.sms_param = "{code:%s}" % captcha
    # request.sms_param = "{username:%s,code:%s}" % (username, captcha)
    request.rec_num = telephone.decode('utf-8').encode('ascii')
    request.sms_template_code = settings.TEMPLATE_CODE
    try:
        resp = request.getResponse()
        cache.set(telephone, captcha, 120)
        return myjson.json_result()
    except Exception, e:
        print e
        return myjson.json_server_error()


@require_http_methods(['GET'])
def qiniu_token(request):
    # 授权
    q = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    # 选择七牛的云空间
    bucket_name = 'myblog-article'
    # 生成token
    token = q.upload_token(bucket_name)
    return myjson.json_result({'uptoken': token})


# 添加文章
def add_article(request, front_or_cms='front'):
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
        return render(request, '%s_add_article.html' % front_or_cms, context)
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
            return render(request, '%s_add_article.html' % front_or_cms, {'error':form.get_error()})
            
# 编辑文章
def edit_article(request, article_id, front_or_cms='front'):
    '''
       它的逻辑和add_article相似，但作者不会变，只需获取文章的id
       我们会用到一篇已存在的article里的的所有数据，包括tags
       但文章里的tags会通过article.tags多对多的方式获取，而不再从tagmodel获取
       因为可能会修改tags，我们仍需要传入所有的tags
       因此我们需要将tags添加到article里，而为了方便使用，也为了添加tags
       我们会使用到model_to_dict这个函数，将数据库里的数据提取出来并转化成dict类型
    '''
    if request.method == 'GET':
        article_model = ArticleModel.objects.filter(pk=article_id).first()
        article_dict = model_to_dict(article_model)
        tag_model = article_model.tags.all()
        article_dict['tags'] = [tag_model.id for tags in tag_model]
        context = {
            'categorys': CategoryModel.objects.all(),
            'tags': TagModel.objects.all(),
            'article': article_dict
        }
        return render(request, '%s_add_article.html' % front_or_cms, context)
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
            return render(request, '%s_edit_article.html' % front_or_cms, {'error':form.get_error()})



# 修改邮箱
def reset_email(request, front_or_cms='front'):
    if request.method == 'GET':
        return render(request, '%s_reset_email.html' % front_or_cms)
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
            return render(request, '%s_reset_email.html'% front_or_cms , {'error':form.get_error()})