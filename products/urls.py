from django.urls import path


from products.views import MainProductView, CoffeeProductView, MainSearchView, ProductDetailView

urlpatterns = [
    path('/main', MainProductView.as_view()),
    path('', CoffeeProductView.as_view()),
    path('/main/search', MainSearchView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]