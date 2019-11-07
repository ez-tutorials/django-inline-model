from django.contrib import messages

# Register your models here.
# from .models import Group, Membership, Person
# from .models import Role, Movie, Artist
# from .models import Book, Author
from .models import Part, Product, Warehouse, Component, Batch, Supplier
from .models import Person, Status, Client, Order, OrderedItem

from django.contrib import admin


class CustomModelAdmin(object):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != 'id'
        ]
        super(CustomModelAdmin, self).__init__(model, admin_site)


class BatchAdmin(admin.ModelAdmin):
    list_display = [
        'number',
        'manufacture_date',
        'manufacture_place',
        'expire_date',
        'supplier'
    ]
admin.site.register(Batch, BatchAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact_person']
    list_filter = (
        'name',
        'address',
        'contact_person',
    )
admin.site.register(Supplier, SupplierAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact_person']
    list_filter = (
        'name',
        'address',
        'contact_person',
    )
admin.site.register(Client, ClientAdmin)


class StatusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Status, StatusAdmin)


class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person, PersonAdmin)


class PartAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'batch', 'warehouse', 'available_total']
    list_filter = (
        'name',
        'batch',
        'batch__manufacture_date',
        'batch__manufacture_place',
        'warehouse',
    )

admin.site.register(Part, PartAdmin)


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1


class ComponentAdmin(admin.ModelAdmin):

    list_display = ['product', 'part', 'unit_quantity']
    list_filter = (
        'product__name',
    )


admin.site.register(Component, ComponentAdmin)


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ComponentInline,
    ]

    list_display = ['name', 'batch', 'packaging_warehouse', 'maximum_available']
    list_filter = (
        'name',
        'batch__number',
        'batch__expire_date',
        'packaging_warehouse',
    )
    search_fields = (
        'name',
        'batch__number'
    )

admin.site.register(Product, ProductAdmin)


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    list_filter = (
        'name',
        'address',
    )


admin.site.register(Warehouse, WarehouseAdmin)


class OrderedItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'order']


admin.site.register(OrderedItem, OrderedItemAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderedItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
    list_display = ['order_name', 'order_number', 'client', 'delivered_by']
    list_filter = (
        'order_number',
        'client',
        'delivered_by'
    )


admin.site.register(Order, OrderAdmin)
