from django.contrib import admin
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
    pass
admin.site.register(Batch, BatchAdmin)


class SupplierAdmin(admin.ModelAdmin):
    pass
admin.site.register(Supplier, SupplierAdmin)


class ClientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Client, ClientAdmin)


class StatusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Status, StatusAdmin)


class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person, PersonAdmin)



class PartAdmin(admin.ModelAdmin):
    pass
admin.site.register(Part, PartAdmin)


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ComponentInline,
    ]


admin.site.register(Product, ProductAdmin)


class WarehouseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Warehouse, WarehouseAdmin)


# class ComponentAdmin(admin.ModelAdmin):
#     pass
#
# admin.site.register(Component, ComponentAdmin)



class OrderedItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity']


admin.site.register(OrderedItem, OrderedItemAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderedItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]

    def save_formset(self, request, form, formset, change):
        # formset has to be saved to get correct queryset
        formset.save()
        # Update part status and quantity available here
        ordered_items = [f if f.quantity != 0 else f for f in formset.queryset]
        for item in ordered_items:
            quantity = item.quantity
            product = item.product
            # Update part total available quantity if all part check passes
        # messages.add_message(request, messages.ERROR, 'Car has been sold')
        super().save_formset(request, form, formset, change)

    def save_model(self, request, obj, form, change):
        # Update order status
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)
