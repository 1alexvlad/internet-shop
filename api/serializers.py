from rest_framework import serializers

from shop.models import Category, Product

from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 'price']
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username']
