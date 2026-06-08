import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','getgig.settings')
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
U=get_user_model()
U.objects.filter(username__in=['c_test','f_test']).delete()
c=U.objects.create_user(username='c_test',password='Pass12345!',user_type='client')
f=U.objects.create_user(username='f_test',password='Pass12345!',user_type='freelancer')
cl=Client(SERVER_NAME='localhost'); cl.login(username='c_test',password='Pass12345!')
for url in ['/projects/client/','/projects/create/','/users/profile/edit/','/users/notifications/']:
    try:
        r=cl.get(url); print('CLIENT',url,r.status_code)
    except Exception as e:
        print('CLIENT ERR',url,type(e).__name__,e)
fl=Client(SERVER_NAME='localhost'); fl.login(username='f_test',password='Pass12345!')
for url in ['/projects/freelancer/','/projects/my-bids/']:
    try:
        r=fl.get(url); print('FREE',url,r.status_code)
    except Exception as e:
        print('FREE ERR',url,type(e).__name__,e)
