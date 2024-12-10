from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishList, name='wishList'),
    path('<int:id>', views.addOrDelWish, name='wishP'),
    path('del<int:id>', views.delWish, name= 'delWish')
]