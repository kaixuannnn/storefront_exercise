from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product

def say_hello(request):
    # sort the queryset
    queryset = Product.objects.order_by('unit_price', '-title').reverse()
    #order with unit price in ascending order and titkle in descending order

    return render(request, 'hello.html', {'name': 'Mosh', 'products':list(queryset)})
