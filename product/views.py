from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductReviewsSerializer


# Category
@api_view(['GET', 'POST'])
def category_list_api_view(request):

    if request.method == 'GET':
        categories = Category.objects.all()

        data = CategorySerializer(categories, many=True).data

        return Response(data=data)
    
    elif request.method == 'POST':
        name = request.data.get('name')

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
        category.name = request.data.get('name')
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
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')

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
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')

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
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product_id')

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
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.product_id = request.data.get('product_id')

        review.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewSerializer(review).data
        )