from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product, OrderItem

def say_hello(request):
    #distinct to remove duplicate item
    productIds =  OrderItem.objects.values('product__id').distinct()
    queryset= Product.objects.filter(id__in=productIds).order_by('title')

    return render(request, 'hello.html', {'name': 'Mosh', 'products':list(queryset)})
