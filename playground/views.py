from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from store.models import Product

def say_hello(request):
    # Products: inventory < 10 OR price <20 
    queryset = Product.objects.filter(Q(inventory__lt=0)|~Q(unit_price__lt=20))
    #~ symbolise Not

    return render(request, 'hello.html', {'name': 'Mosh', 'products':list(queryset)})
