from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField() # HW 2
    
    class Meta:
        model = Category
        fields = 'id name products_count'.split()
        
    def get_products_count(self, obj):
        return obj.product_set.count()
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
# HW 2
class ProductReviewsSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = 'id title price reviews'.split()