//验证码刷新
$("#valid_img").click(function () {
    $(this)[0].src+="?"
});

// ajax请求验证
$("#login_but").click(function () {
   $.ajax({
       url:"/login/",
       type:"post",
       data:{
           "user":$("#user").val(),
           "pwd":$("#pwd").val(),
           "valid_cod":$("#valid").val(),
           "csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val(),
       }

   })
});






