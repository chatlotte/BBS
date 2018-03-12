# 数据库表设计   
**在models.py中我们定义了所使用的数据库所用的表，这里进行简单的分析.**   

UserInfo   用户表  
Blog       个人站点信息表  
Category   博客个人文章分类  
Tag        标签  
Article    文章  
ArticleDetail    文章详细表  
Comment    评论表  
ArticleUpDown    点赞表  
Article2Tag      自己创建的第三章表  

**注释：**  
我们可以分析：UserInfo和Blog是一对一的关系；一个人只能有一个主页；  
Blog和Category是一对多的关系，一个用户可以有多个分类；它和Tag标签的原理是一样的；  
Category和Article是一对多的关系，一类文章可以有多个文章；  
Tag和article表是多对多的关系，一篇文章可以有多个标签；  
这里把UserInfo和Article表建立关系，这里需要注意的是：在数据库层面上我们尽量减少跨表。他是一对多的关系；  





