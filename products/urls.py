from django.urls import path

from products.views import MainProductView, CoffeeProductView, ProductDetailView

urlpatterns = [
    path('/main', MainProductView.as_view()),
    path('', CoffeeProductView.as_view()),
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
]