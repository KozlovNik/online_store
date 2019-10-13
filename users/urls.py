from django.urls import path
from users import views


urlpatterns = [
    path('sign_out/', views.sign_out, name='sign_out'),
]
