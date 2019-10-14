from django.urls import path
from store_app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('change_item_quantity/', views.change_item_quantity, name='change_quantity'),
    path('catalog/', views.show_catalog, name='catalog'),
    path('favorites/', views.show_favorites, name='favorites'),
    path('is_authenticated/', views.is_user_authenticated, name='is_authenticated'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    path('catalog/<category_slug>/', views.show_category, name='cat'),
    path('catalog/<category_slug>/<product_slug>/', views.show_product, name='product'),
]
