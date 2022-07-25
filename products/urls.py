from django.urls import path

from products.views import MainProductView, CoffeeProductView

urlpatterns = [
    path('/main', MainProductView.as_view()),
    path('', CoffeeProductView.as_view()),
]