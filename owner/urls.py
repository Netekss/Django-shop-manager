from django.urls import path
from . import views

urlpatterns = [
    # owner menu
    path('menu', views.index, name='owner_index'),
    # auth
    path('register/', views.register_page, name='register'),
]
