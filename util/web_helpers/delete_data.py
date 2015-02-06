# -*- coding: utf8 -*-
import logging
import sys
import datetime

from django.core.management import setup_environ

sys.path.append('/Users/yuguo163/workspace/test/zhiqu') 

import settings
setup_environ(settings)

from apps.cc.models import Files

def delete_data():
    last_two_week_date = datetime.datetime.now()-datetime.timedelta(days=14)
    Files.objects.filter(create__lt=last_two_week_date).delete()
    return 



if __name__ == '__main__':
    delete_data()



