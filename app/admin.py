from django.contrib import messages

# Register your models here.
# from .models import Group, Membership, Person
# from .models import Role, Movie, Artist
# from .models import Book, Author
from .models import Part, Product, Warehouse, Component, Batch, Supplier
from .models import Person, Status, Client, Order, OrderedItem

from django.contrib import admin
from django import forms


class InlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InlineForm, self).__init__(*args, **kwargs)



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
    list_display = ['name', 'part_code', 'batch', 'warehouse', 'available_total']
    list_filter = (
        'name',
        'batch',
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

    list_display = ['name', 'product_code', 'batch', 'packaging_warehouse', 'maximum_available']
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
    list_filter = (
        'order__order_name',
        'product__name',
        'order__client'
    )


admin.site.register(OrderedItem, OrderedItemAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderedItem
    extra = 1
    # form = InlineForm

    # def get_formset(self, request, obj=None, **kwargs):
    #     InlineForm.obj = obj
    #     return super(OrderItemInline, self).get_formset(request, obj, **kwargs)

        # return formset


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

    def save_formset(self, request, form, formset, change):
        parts_needed = {}
        for item in formset:
            if item.instance.product_id:
                ordered_product = item.instance.product
                ordered_quantity = item.instance.quantity
                for comp in Component.objects.filter(product=ordered_product):
                    if comp.part not in parts_needed:
                        parts_needed.update(
                            {
                                comp.part: ordered_quantity * comp.unit_quantity
                            }
                        )
                    else:
                        parts_needed[comp.part] += ordered_quantity * comp.unit_quantity
        submit_order = True
        for part, total_quantity_needed in parts_needed.items():
            if part.available_total < total_quantity_needed:
                messages.add_message(
                    request,
                    messages.WARNING,
                    f"Part: [{part.name} - {part.batch.number}] short: {total_quantity_needed - part.available_total}"
                )
                submit_order = False
        # if submit_order:
        return super().save_formset(request, form, formset, change)




admin.site.register(Order, OrderAdmin)
