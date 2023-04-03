from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category, Review
from .serializers import ProductSerializer, ReviewSerializer, CategorySerializer, RatingSerializer,CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer

'''PRODUCTS'''

@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)
    else:
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
        product = Product.objects.create(title=title, description=description, price=price,
                                          category_id=category_id, tags=tags)
        product.tags.set(tags)
        return Response(data=ProductSerializer(product).data)
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Object not found!'})

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = request.data.get('category_id')
        tags = serializer.validated_data.get('tags')
        product.tags.set(tags)
        product.save()
        return Response(data=ProductSerializer(product).data)

'''RATING'''

@api_view(['GET', 'POST'])
def products_reviews_rating_view(request):
    products = Product.objects.all()
    serializer = RatingSerializer(products, many=True)
    return Response(data=serializer.data)


'''CATEGORY'''

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data)
    else:
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        name = serializer.validated_data.get('name')
        category = Category.objects.create(name=name)
        return Response(data=CategorySerializer(category).data)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Object not found!'})

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(data=serializer.data)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get('name')
        return Response(data=CategorySerializer(category).data)


'''REVIEW'''

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')
        review = Review.objects.create(text=text, stars=stars,
                                       product_id=product_id)
        return Response(data=ReviewSerializer(review).data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Object not found!'})
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.product_id = request.data.get('product_id')
        return Response(data=ReviewSerializer(review).data)