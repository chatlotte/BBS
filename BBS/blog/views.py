from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.http import JsonResponse
from django.forms import widgets
from django import forms
from .models import *
def login(request):
    '''
    登陆页面
    :param request: 用户名密码
    :return: login_response字典里的数据
    '''
    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        input_valid_codes=request.POST.get("valid_code")
        keep_valid_codes=request.session.get("keep_valid_codes")
        login_response={"user":None,"error_msg":""}
        if keep_valid_codes.upper()==input_valid_codes.upper():
            user=auth.authenticate(username=user,password=pwd)
            if user:
                auth.login(request,user)
                login_response["user"]=user.username
            else:
                login_response["error_msg"] = "username or password error!"
        else:
            login_response["error_msg"]="valid_code error!"
        import json
        return HttpResponse(json.dumps(login_response))
    else:
        return render(request,"login.html")
def get_valid_img(request):
    '''
    获取验证码
    :param request:
    :return: 验证码图片
    '''
    from blog.utils import valid_code
    data=valid_code.get_valid_value(request)
    return HttpResponse(data)
class RegForm(forms.Form):
    '''
    利用form组件处理后端表单
    '''
    user=forms.CharField(min_length=4,
                widget=widgets.TextInput(attrs={"class":"form-control"})
                         )
    pwd=forms.CharField(
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    repeat_pwd=forms.CharField(
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    email=forms.EmailField(
        widget=widgets.EmailInput(attrs={"class": "form-control"})
    )
def register(request):
    '''
    注册页面处理提交信息
    :param request:
    :return:
    '''
    #      print("request.POST",request.POST)   # <QueryDict: {'user': ['123'], 'pwd': ['1231'], 'repeat_pwd': ['1231'], 'email': ['123'], 'csrfmiddlewaretoken': ['PjMKenIgrFYWY52U5EcYbkfmib2EiMzK19K5xv4qBon5XZbPDkuiMhMf2LqaV2wy']}>
    #     print("request.FILES",request.FILES) # request.FILES <MultiValueDict: {'avatar_img': [<InMemoryUploadedFile: linhaifeng.jpg (image/jpeg)>]}>

    if request.is_ajax():
        form_obj = RegForm(request.POST)
        reg_response = {"user":None,"error_mes":None}
        if form_obj.is_valid():
            user = form_obj.cleaned_data.get("user")
            pwd = form_obj.cleaned_data.get("pwd")
            email = form_obj.cleaned_data.get("email")
            avatar_img = request.FILES.get("avatar_img")
            if avatar_img:
                user = UserInfo.objects.create_user
            else:
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email)
            reg_response["user"]=user.username
        else:
            reg_response["error_mes"]=form_obj.errors
        return JsonResponse(reg_response)
    else:
        # 实例化form组件的类
        form_obj=RegForm()
        return render(request,"reg.html",{"form_obj":form_obj})
def index(request):
    article_list = Article.objects.all()
    print(article_list)
    return render(request,"index.html",{"article_list":article_list})
def log_out(request):
    auth.logout(request)
    return redirect("/index/")

def home_site(request,username,**kwargs):
    '''
    个人站点设计
    :param request: 请求数据对象
    :return:
    '''
    print("kwargs",kwargs)
    print(username)
    user=UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("<h3>404</h3>")

    # 当前访问站点对象
    blog=user.blog
    # 当前访问站点的所有文章
    if not kwargs:
        article_list=Article.objects.filter(user=user)
    else:
        condition=kwargs.get("condition")
        param=kwargs.get("param") # 2018-02
        if condition=="cate":
             article_list = Article.objects.filter(user=user).filter(homeCategory__title=param)
        elif condition=="tag":
            article_list = Article.objects.filter(user=user).filter(tags__title=param)
        else:
            year,month=param.split("-")
            article_list = Article.objects.filter(user=user).filter(create_time__year=year,create_time__month=month)

    return render(request,"blog/home_site.html",locals())




def article_detail(request,username,article_id):

    article_obj=Article.objects.filter(pk=article_id).first()

    comment_list=Comment.objects.filter(article_id=article_id)
    return render(request,"blog/artcile_detail.html",{"article_obj":article_obj,"username":username,"comment_list":comment_list})

###########################################
import json
from django.db.models import F
from django.http import JsonResponse

from django.db import transaction

def up_down(request):
    print(request.POST)

    article_id=request.POST.get("article_id")
    is_up=json.loads(request.POST.get("is_up"))
    user_id=request.user.pk
    print(is_up)

    res={"state":True,"err":""}
    try:
        # 处理事务
        with transaction.atomic():
            obj=ArticleUpDown.objects.create(user_id=user_id,article_id=article_id,is_up=is_up)
            if is_up:
                 Article.objects.filter(pk=article_id).update(up_count=F('up_count')+1)
            else:
                Article.objects.filter(pk=article_id).update(down_count=F('down_count') + 1)
    except Exception as e:
        obj=ArticleUpDown.objects.filter(user_id=user_id,article_id=article_id).first()
        res["state"]=False
        res["err"]=obj.is_up

    return JsonResponse(res)



def comment(request):
    content=request.POST.get('content')
    article_id=request.POST.get('article_id')
    pid=request.POST.get('pid')
    user_id=request.user.pk
    res={}
    with transaction.atomic():
        if pid: # 保存子评论
            obj = Comment.objects.create(content=content, article_id=article_id, user_id=user_id,parent_comment_id=pid)
        else: # 保存根评论
            obj = Comment.objects.create(content=content, article_id=article_id, user_id=user_id)

        Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)
    res["create_time"]=obj.create_time.strftime("%Y-%m-%d %H:%M")
    res["content"]=obj.content
    return JsonResponse(res)




def backend(reqeust):
    username=reqeust.user

    article_list=Article.objects.filter(user=reqeust.user)


    return render(reqeust,"blog/backend.html",locals())

def add_article(reqeust):

    username=reqeust.user.username
    return render(reqeust,"blog/add_article.html",locals())

def upload_img(reqeust):
    print(reqeust.FILES)
    obj=reqeust.FILES.get("put_img")
    name=obj.name

    from cnblog_s19 import settings
    import os
    path=os.path.join(settings.MEDIA_ROOT,"add_article_img",name)

    f=open(path,"wb")

    for line in obj:
        f.write(line)
    f.close()

    res={
        "url":"/media/add_article_img/"+name,
        "error":0
    }
    import json
    return HttpResponse(json.dumps(res))







