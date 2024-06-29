from django.urls import path
from .views import ESOKOView,category_products
urlpatterns = [
   path('',ESOKOView.as_view(),name='esoko'),
   path('<uuid:id>', ESOKOView.as_view(),name='single_product'),
   path('products/<uuid:id>', category_products,name='category_products'),
]