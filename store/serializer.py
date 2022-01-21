from rest_framework import serializers

#serializer -  can use it to convert a product object to a Python dictionary
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title =  serializers.CharField(max_length=255)
    unit_price =  serializers.DecimalField(max_digits=6, decimal_places=2)