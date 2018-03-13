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
       },
       success:function (data) {
           var data=JSON.parse(data);
           if (data.user){
               // 登陆成功
               location.href="/index/"

           }
           else {
               $(".error").html(data.error_msg).css("color","red")
               setTimeout(function () {
                   $(".error").html("")
               },1000)
           }
       }

   })
});






