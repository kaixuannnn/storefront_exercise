from cgitb import lookup
from django.contrib import admin, messages
from django.http import HttpRequest

from tags.models import TaggedItem
from . import models
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.contrib.contenttypes.admin import GenericTabularInline

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin) :
        return [
            ('<10','Low')
        ]
    
    def queryset(self, request, queryset) :
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions=['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_id']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    #like models, we can also preselect/ preload the collection
    list_select_related = ['collection']
    search_fields=['title']
    inlines = [TagInline]

    def collection_id(self, product):
        return product.collection.id

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
       updated_count =  queryset.update(inventory=0)
       self.message_user(
           request,
           f'{updated_count} products were successfully updated!',
           messages.ERROR
       )

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields=['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({
            'collection__id': str(collection.id)
        })
        return format_html('<a href="{}">{}</>',url,collection.products_count)

    def get_queryset(self, request: HttpRequest) :
        return super().get_queryset(request).annotate(products_count=Count('product'))

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

#we also have StackInline
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num =1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]