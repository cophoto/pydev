from django.urls import path, re_path
from sign import views_if

urlpatterns = [
    re_path(r'^add_event/', views_if.add_event, name='add_event'),
    re_path(r'^get_event_list/', views_if.get_event_list, name='get_event_list'),
]