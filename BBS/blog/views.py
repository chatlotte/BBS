from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.http import JsonResponse
def login(request):
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
    from blog.utils import valid_code
    data=valid_code.get_valid_value(request)
    return HttpResponse(data)
