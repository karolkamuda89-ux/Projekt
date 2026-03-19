from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('list/', views.file_list, name='list'),
    path('detail/<int:plik_id>/', views.detail, name='detail'),
]