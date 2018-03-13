// ajax请求验证
$("#reg_btn").click(function () {
   var form_data = new FormData();
   form_data.append("user",$("#id_user").val());
   form_data.append("pwd",$("#id_pwd").val());
   form_data.append("repeat_pwd",$("#id_repeat_pwd").val());
   form_data.append("email",$("#id_email").val());
   form_data.append("csrfmiddlewaretoken",$("[name='csrfmiddlewaretoken']").val());
   form_data.append("avatar_img",$("#avatar")[0].files[0]);
    $.ajax({
        url:"/register/",
        type:"post",
        processData:false,    // processData 默认为false，当设置为true的时候,jquery ajax 提交的时候不会序列化 data，而是直接使用data
        contentType:false,
        data:form_data,
        success:function (data) {  // {"user":","error_meg":""}
            if (data.user){  // 注册失败
                var errors_dic=data.error.error_mes;
                // 清空操作
                $("form span").html("");
                $(".form-group").removeClass("has-error");
                $.each(errors_dic,function (field,error_info) {
                    $("#id_"+field).next().html(error_info[0]).css("color","red");
                    $("#id_"+field).parent().addClass("has-error");

                })

            }

        }
    })
});
// 头像预览
$("#avatar").change(function () {
   // 获取用户选中的文件
   var choose_file = $("#avatar")[0].files[0];
   // JS的文件阅读器
    var reader = new FileReader();
    reader.readAsDataURL(choose_file);
    reader.onload = function () {
        $("#avatar_img").attr("src",this.result)
    };
});






