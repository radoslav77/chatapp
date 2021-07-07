from django.urls import path
from . import views

# urls path
urlpatterns = [
    path('', views.index, name='index'),
]
