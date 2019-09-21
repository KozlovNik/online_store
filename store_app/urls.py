from django.urls import path
from store_app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_view, name='cart'),
    path('<category_slug>/', views.show_category, name='cat'),
    path('add_to_cart/<slug>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/<slug>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('<category_slug>/<product_slug>/', views.show_product, name='product'),
]
