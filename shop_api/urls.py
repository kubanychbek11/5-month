from django.contrib import admin
from django.urls import path, include
from product import views
from . import swagger
urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/categories/', views.CategoryListApiVIew.as_view()),
    path('api/v1/categories/<int:id>/', views.CategoryDetailApiVIew.as_view()),

    path('api/v1/products/', views.ProductListApiView.as_view()),
    path('api/v1/products/<int:id>/', views.ProductDetailListApiView.as_view()),

    path('api/v1/reviews/', views.ReviewListApiView.as_view()),
    path('api/v1/reviews/<int:id>/', views.ReviewDetailListApiView.as_view()),

    path('api/v1/products/reviews/', views.products_reviews_rating_view),
    #path('api/v1/products/reviews/', views.ProductsReviewsRatingView.as_view()),

    path('api/v1/users/', include('users.urls'))
]
urlpatterns += swagger.urlpatterns