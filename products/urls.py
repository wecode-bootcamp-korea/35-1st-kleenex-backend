from django.urls import path

from products.views import MainProductView

urlpatterns = [
    path('/main', MainProductView.as_view()),
]