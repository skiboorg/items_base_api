
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import exceptions, serializers, status, generics
from .models import *
from user.serializers import UserSaveSerializer

from django.contrib.auth.tokens import default_token_generator


import logging
logger = logging.getLogger(__name__)



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'


class IzdelieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Izdelie
        fields = '__all__'

class ProductSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSupply
        fields = '__all__'

class ProductRemoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRemove
        fields = '__all__'



class ProductSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    supplies = ProductSupplySerializer(many=True, required=False, read_only=True)
    removes = ProductRemoveSerializer(many=True, required=False, read_only=True)

    category = CategorySerializer(many=False, required=True, read_only=False)
    subcategory = SubCategorySerializer(many=False, required=True, read_only=False)
    izdelie = IzdelieSerializer(many=False, required=True, read_only=False)

    class Meta:
        model = Product
        fields = '__all__'

    # def create(self, validated_data):
    #     print(validated_data)
    #     category_data = validated_data.pop('category')
    #
    #     # order = Order.objects.create(**validated_data)
    #     return














