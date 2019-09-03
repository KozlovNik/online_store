from django.urls import path
from store_app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<category_slug>/', views.show_category, name='cat'),
    path('<category_slug>/<product_slug>/', views.show_product, name='product'),
]
