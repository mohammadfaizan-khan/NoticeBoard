from django.urls import path
from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('notice/new/', views.create_notice, name='create_notice'),
    path('notice/<int:pk>/delete/', views.delete_notice, name='delete_notice'),
]