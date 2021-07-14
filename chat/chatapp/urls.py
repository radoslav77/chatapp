from django.urls import path
from . import views

# urls path
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('register', views.register, name='register'),
    path('post/<str:username>', views.post, name='post'),
    path('home', views.home, name='home'),
    path('chat/<str:username>', views.chat, name='chat'),
    path('delete/<int:id>/<str:username>', views.delete, name='delete'),

    # api
    path('chat_api/<str:username>', views.chat_api, name='chat_api')

]
