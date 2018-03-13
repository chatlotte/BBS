# 浅谈contentType = false  
文件位置:项目/blog/static/js/reg.js   

contentType简单说它是代表发送信息到服务器内容编码类型，通俗来说就是告诉服务器从浏览器提交过来得数据格式。  
默认值为contentType = "application/x-www-form-urlencoded".在默认情况下，内容编码类型满足大多数情况。    
在这里我们谈一下contentType = false.  
在使用ajax上传文件时：   
```javascript
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
    })



});

```
这里封装了一个FormData对象，然后我们用post方法传给服务器。   
当我们使用表单上传文件时，我们来查看它的request headers:   
Content-Type:multipart/form-data;boundary=---WebKitFormBoundaryuwYcfA2AlgxqlxAO   
在multipart/form-data后边有boundary以及一串字符，这是分界符，后边时一对随机生成的字符串，目的时防止上传文件中出现分界符导致服务器无法正确识别文件开始位置。  
对于上传文件l，我们没有在使用原有的HTTP协议，所以multipart/form-data请求是基于HTTP原有的请求方式post而来的。   
全新请求方式与post的区别  
> - 1 请求头的不同，对于上传的文件，contentType = multipart/form-data是必须的，而post则不是，毕竟post又不是只上传文件。  
> - 2 请求体不同。这里的不同也就是指前者在发送的每个字段内容之间必须要使用分隔符来隔开，比如文件内哦让那个和文本的内容就需要隔开，不然服务器就没有办法正常的解析文件，而后者post当然就没有分界符直接以name = "value"的形式发送。  

在jquery ajax()方法中我们使用contentType = false,是为了避免jquery对其操作，从而失去分界符，而使服务器不能正常解析文件。


