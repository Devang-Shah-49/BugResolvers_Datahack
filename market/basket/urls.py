from django.urls import path
from .views import *

urlpatterns = [
    path('get_user',get_user,name='get_user'),
    path('send_codes/',send_codes,name='send_codes'),
    path("get_data", get_data, name="get_data"),
    path("get_query", get_query, name="get_query"),
    path("get_rfm", rfm_table, name="get_rfm"),
    path("get_charts", get_charts, name="get_charts"),
    path("get_stats", get_stats, name="get_stats"),
]