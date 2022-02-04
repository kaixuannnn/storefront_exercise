from decimal import Decimal
from site import check_enableusersite

from rest_framework import serializers

from store.models import Cart, CartItem, Product, Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Collection
        fields = ['id', 'title', 'products_count']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length = 255)
    products_count = serializers.IntegerField(read_only=True)

#serializer -  can use it to convert a product object to a Python dictionary
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        #Besides, we can show all the field by doing this, however, it is not recommended, we dont want all the field to be exposed to outside world
        #fields = '__all__'
        # all the code below can be eliminated
        fields = ['id', 'title','description', 'slug','inventory','unit_price', 'price_with_tax','collection']
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

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date','name','description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
   class Meta:
       model = Product
       fields = ['id','title','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta: 
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No prduct with the given id was found')
        return value

    # In this case, we cant get the cart id from the url,
    # in order to get the cart id, we need to go to the view and get the cart id from the context
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
      return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id','items','total_price']

