from django.urls import path

from products.views import CoffeeProductView

urlpatterns = [
    path('', CoffeeProductView.as_view()),
    path('/<int:coffee_category_id>', CoffeeProductView.as_view()),
]