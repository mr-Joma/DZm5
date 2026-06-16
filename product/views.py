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
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# Category
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryValidateSerializer
        return self.serializer_class


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CategoryValidateSerializer
        return self.serializer_class
    

# Product
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        return self.serializer_class


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProductValidateSerializer
        return self.serializer_class



# HW 2
@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()

    data = ProductReviewsSerializer(products, many=True).data

    return Response(data=data)



# Review
class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewValidateSerializer
        return self.serializer_class


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ReviewValidateSerializer
        return self.serializer_class