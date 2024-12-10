from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.myCart, name='myCart'),
    path('delete/<int:id>/', views.deleteProductCart, name='deleteProductCart'),
    path('addCart/<int:id>/', views.addProductToCart, name = 'addProductToCart'),
    path('createOrder', views.createOrder, name='createOrder'),
    path('fullDeleteCart',views.fullDeleteCart, name='fullDeleteCart'),
    path('plusorminus/<int:id>/<str:sign>', views.plusOrMinusCart, name='plusOrMinusCart'),
]