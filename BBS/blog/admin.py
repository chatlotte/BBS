from django.contrib import admin
from .models import *
'''
django为我们提供一个web界面操纵数据库,需要创建超级管理员去操作
python3 manage.py createsuperuser
'''

admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(ArticleDetail)
admin.site.register(ArticleUpDown)
admin.site.register(Comment)
admin.site.register(Article2Tag)



