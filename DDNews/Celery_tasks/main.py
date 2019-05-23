from celery import Celery

#为cerely使用Django配置文件进行设置

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'DDNews.settings.dev'

#创建celery应用

app = Celery('panda_new')

#导入celery配置(使用redis几号库存储book信息)
app.config_from_object('Celery_tasks.config')

#自动注册celery任务
app.autodiscover_tasks(['Celery_tasks.sms'])