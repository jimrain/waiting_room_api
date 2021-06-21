from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers

urlpatterns = [
    path('api/queue_info/', views.queue_info_list),
    path('api/queue_info/<int:pk>/', views.queue_info_detail),
    path('api/user_info/', views.user_info_list),
    path('api/user_info_checkin/<int:pk>/', views.user_info_checkin),
    path('api/queue_position/', views.user_queue_position),
]
# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'accounts', views.AccountViewSet)
# router.register(r'videos', views.VideoViewSet)
#
# app_name = 'pmvc'
#
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('api/', include(router.urls)),
#     path('api/aes128key/', views.aes128key_create),
#     path('api/aes128key/<int:pk>', views.aes128key_detail),
# ]
#
