from django.urls import path
from store_app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('change_item_quantity/', views.change_item_quantity, name='change_quantity'),
    path('<category_slug>/', views.show_category, name='cat'),
    path('<category_slug>/<product_slug>/', views.show_product, name='product'),
]
