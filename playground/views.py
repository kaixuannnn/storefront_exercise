from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product, OrderItem

def say_hello(request):

    queryset= Product.objects.prefetch_related('promotions').select_related('collection').all()
    #in this case, django is not going to query the related tables unless we speicifically instructed to do so
    # preload the data

    return render(request, 'hello.html', {'name': 'Mosh', 'products':list(queryset)})
