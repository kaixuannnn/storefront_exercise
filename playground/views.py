from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product

def say_hello(request):
    # Products: inventory = price
    queryset = Product.objects.filter(inventory=F('collection__id'))
    #~ symbolise Not

    return render(request, 'hello.html', {'name': 'Mosh', 'products':list(queryset)})
