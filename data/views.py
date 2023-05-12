import json

import django_filters
from django_filters import IsoDateTimeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers

from PIL import Image, ImageDraw, ImageFont


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        setattr(request.data, '_mutable', True)
        try:
            request.data.pop('files')
            files_descriptions = request.data.pop('descriptions')
        except:
            files_descriptions = []
        data = json.loads(json.dumps(request.data))
        json_data = {}
        for dat in data:
            json_data[dat] = json.loads(data[dat])
        serializer = self.get_serializer(data=json_data)
        if serializer.is_valid():
            order = serializer.save()
            order.created_by = request.user
            order.save()
            # for index,file in enumerate(request.FILES.getlist('files')):
            #     OrderFile.objects.create(file=file,order=order,description=files_descriptions[index])
        else:
            print(serializer.errors)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        setattr(request.data, '_mutable', True)
        try:
            request.data.pop('files')
            files_descriptions = request.data.pop('descriptions')
        except:
            files_descriptions = []
        data = json.loads(json.dumps(request.data))
        json_data = {}
        for dat in data:
            json_data[dat] = json.loads(data[dat])
        print(json_data)
        serializer = self.get_serializer(instance, data=json_data)
        if serializer.is_valid():
            order = serializer.save()
            # for index, file in enumerate(request.FILES.getlist('files')):
            #     OrderFile.objects.create(file=file, order=order, description=files_descriptions[index])
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class GetCategories(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class AddRemove(APIView):
    def post(self,request):
        print(request.data)
        ProductRemove.objects.create(
            product_id=request.data['id'],
            amount=int(request.data['data']['amount']),
            text=request.data['data']['text'],
            is_remove=request.data['data']['is_remove'],
                                     )
        return Response(status=200)


class AddSupply(APIView):
    def post(self,request):
        ProductSupply.objects.create(
            product_id=request.data['id'],
                                     amount=int(request.data['data']['amount']),
                                     text=request.data['data']['text'],
                                     )
        return Response(status=200)

class GetProductByUuid(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        return Product.objects.get(uuid=self.request.query_params.get('uuid'))


