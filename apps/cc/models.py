# -*- encoding=utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User

#文本上传
class Files(models.Model):
    url = models.CharField(max_length=128,verbose_name=u'url')
    create = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'files'
        ordering = ['-create']
