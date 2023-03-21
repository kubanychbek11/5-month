from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from rest_framework import status


@api_view(['GET'])
def category_list_api_view(request):
    category = Category.objects.all()
    serializer = Category(category, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Object not found!'})
    serializer = CategorySerializer(category)
    return Response(data=serializer.data)

@api_view(['GET'])
def product_list_api_view(request):
    product = Product.objects.all()
    serializer = Product(product, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Object not found!'})
    serializer = ProductSerializer(product)
    return Response(data=serializer.data)

@api_view(['GET'])
def review_list_api_view(request):
    review = Review.objects.all()
    serializer = Review(review, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Object not found!'})
    serializer = ReviewSerializer(review)
    return Response(data=serializer.data)
