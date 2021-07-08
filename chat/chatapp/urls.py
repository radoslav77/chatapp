from django.urls import path
from . import views

# urls path
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('register', views.register, name='register'),
    path('post', views.post, name='post'),
]
