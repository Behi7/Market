from django.urls import path
from . import views

urlpatterns = [
    path('list', views.listProduct, name='listProduct'),
    path('shop', views.productlists, name='shop'),
    path('<slug:slugCategory>/<slug:slugsubcategory>/<slug:slugproduct>', views.detailProduct, name='product_detail'),
    path('<slug:slugCategory>/<slug:slugsubcategory>', views.categorysubcategorylisyt, name='categorysubcategorylist'),
    path('<slug:slugCategory>', views.categoryProductlist, name='categoryProductlist'),
    path('addCart/<int:id>/', views.addProductToCart, name = 'addtToCart'),
]