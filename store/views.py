from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Collection, OrderItem, Product, Review
from .serializer import CollectionSerializer, ProductSerializer, ReviewSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['collection_id']

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                    {
                    'error': 'Product cannot be deleted because it is associated with an order item.'
                    }, 
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                    )
        return super().destroy(request, *args, **kwargs)

# we no more longer need the ProductList and ProductDetailView

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')), pk=pk 
            )
        if collection.products.count() > 0:
            return Response(
                {
                    'error':'Collection cannot be deleted because it includes one or more products.'
                }, 
                status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}