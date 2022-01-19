from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product




def say_hello(request):
    exists = Product.objects.filter(pk=1).exists()
    #return bolean

    return render(request, 'hello.html', {'name': 'Mosh'})
