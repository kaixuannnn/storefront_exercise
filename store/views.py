from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Collection, Product
from .serializer import CollectionSerializer, ProductSerializer

class ProductList(APIView):
    def get(self, request, ):
        queryset = Product.objects.select_related('collection').all()
        serializer= ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CollectionDetail(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')), pk=pk 
            )
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    def put(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')), pk=pk 
            )
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer,data=request.data)
    def delete(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')), pk=pk 
            )
        if collection.products.count() > 0:
            return Response({'error':'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)