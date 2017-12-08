from .models import Product, Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Review
        fields = ('id', 'title', 'review', 'rating', 'created_by')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price')
