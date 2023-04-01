from django.urls import path
from .views import *

urlpatterns = [
    path('get_user',get_user,name='get_user'),
    path('send_codes/',send_codes,name='send_codes'),
]