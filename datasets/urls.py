from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('list/', views.file_list, name='list'),
    path('detail/<int:plik_id>/', views.detail, name='detail'),
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
]