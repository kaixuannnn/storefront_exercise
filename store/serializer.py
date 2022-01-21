from decimal import Decimal

from rest_framework import serializers

from store.models import Product, Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Collection
        fields = ['id', 'title']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length = 255)

#serializer -  can use it to convert a product object to a Python dictionary
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        #Besides, we can show all the field by doing this, however, it is not recommended, we dont want all the field to be exposed to outside world
        #fields = '__all__'
        # all the code below can be eliminated
        fields = ['id', 'title', 'unit_price', 'price_with_tax','collection']
    # id = serializers.IntegerField()
    # title =  serializers.CharField(max_length=255)
    # price =  serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.PrimaryKeyRelatedField(queryset = Collection.objects.all())
    # Besides, we can also get string related field
    # collection = serializers.StringRelatedField()
    # we can do it in nested field
    # collection =  CollectionSerializer()
    # view_name is the field that we use to ctreate the hyperlink
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection_detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)