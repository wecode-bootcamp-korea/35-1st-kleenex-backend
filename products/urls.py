from django.urls import path

from products.views import MainProductView, CoffeeProductView, MainSearchView

urlpatterns = [
    path('/main', MainProductView.as_view()),
    path('', CoffeeProductView.as_view()),
    path('/main/test', MainSearchView.as_view())
]