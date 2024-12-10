from django.urls import path
from . import views

urlpatterns = [
    path('create', views.createBanner, name='create'),
    path('list', views.listBanner, name='list'),
    path('delete/<int:id>', views.deleteBanner, name='delete')
]