from django.db import models
# 数据库表名User，继承了models.Model
class User(models.Model):
    """
    CharField 相当于varchar
    DateField 相当于datetime
    max_length 参数限定长度
    unique  是否唯一
    """
    name = models.CharField(max_length=128,unique=True)
