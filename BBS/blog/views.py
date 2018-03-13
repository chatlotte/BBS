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




    return






