from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ReviewSerializer, 
    ProductReviewsSerializer,
    CategoryValidateSerializer,
    ProductValidateSerializer,
    ReviewValidateSerializer
)


# Category
@api_view(['GET', 'POST'])
def category_list_api_view(request):

    if request.method == 'GET':
        categories = Category.objects.all()

        data = CategorySerializer(categories, many=True).data

        return Response(data=data)
    
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)# HW 4

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data=serializer.errors)

        name = serializer.validated_data.get('name')#

        category = Category.objects.create(
            name=name
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=CategorySerializer(category).data
        )

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = CategorySerializer(category, many=False).data
        
        return Response(data=data)
    
    elif request.method == 'DELETE':
        category.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data) # HW 4

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        category.name = serializer.validated_data.get('name')#
        category.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=CategorySerializer(category).data
        )

    

# Product
@api_view(['GET', 'POST'])
def product_list_api_view(request):
    
    if request.method == 'GET':
        products = Product.objects.all()

        data = ProductSerializer(products, many=True).data

        return Response(data=data)

    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data) # HW 4

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')#

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductSerializer(product).data
        )

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ProductSerializer(product, many=False).data

        return Response(data=data)
    
    elif request.method == 'DELETE':
        product.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)# HW 4

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
            
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')#

        product.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductSerializer(product).data
        )



# HW 2
@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()

    data = ProductReviewsSerializer(products, many=True).data

    return Response(data=data)



# Review
@api_view(['GET', 'POST'])
def review_list_api_view(request):

    if request.method == 'GET':
        reviews = Review.objects.all()

        data = ReviewSerializer(reviews, many=True).data

        return Response(data=data)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)# HW 4

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')#

        review = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewSerializer(review).data
        )


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewSerializer(review, many=False).data

        return Response(data=data)

    elif request.method == 'DELETE':
        review.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)# HW 4

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
                
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')#

        review.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewSerializer(review).data
        )