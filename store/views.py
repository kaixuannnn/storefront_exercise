from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializer import ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        # many = True, the serializer knows that ut should iterate over this query set and 
        # convert each product object to a dictionary
        serializer= ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        # before we send the data to post, we need to validate the data
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok')
        # else: 
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # other than if else, we can use raise_exception to write a clearer code
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data
        # if you print(serializer.validated_data), it returns the dictionary of the object
        # when saving the data, we no need to call the serializer.validated_data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PUT', 'PATCH'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        # product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view()
def collection_detail(request, pk):
    return Response('OK')