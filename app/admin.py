from django.contrib import messages

# Register your models here.
# from .models import Group, Membership, Person
# from .models import Role, Movie, Artist
# from .models import Book, Author
from .models import Part, Product, Warehouse, Component, Batch, Supplier
from .models import Person, Status, Client, Order, OrderedItem, PartOrdered

from django.contrib import admin
from .forms import *


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
    list_filter = (
        'number',
        'manufacture_date',
        'manufacture_place',
        'expire_date',
        'supplier__name'
    )
    search_fields = (
        'number',
        'manufacture_date',
        'manufacture_place',
        'expire_date',
        'supplier__name'
    )
   #  This is for arrange how fields are displayed in admin page
   #  fieldsets = (
        # ('Company', {
        #     'fields': ('company',),
        # }),
        # ('Partner Service', {
        #     'fields': ('vendor_id', 'name', 'max_app_limit'),
        # }),
   #  )

admin.site.register(Batch, BatchAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact_person']
    list_filter = (
        'name',
        'address',
        'contact_person',
    )
    search_fields = (
        'name',
        'address',
    )
    form = SupplierAdminForm
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
    list_display = ['name', 'part_code', 'batch', 'warehouse', 'available', 'total']
    list_filter = (
        'name',
        'batch',
        'warehouse',
    )
    search_fields = (
        'name',
        'part_code',
        'batch__number',
        'warehouse__name',
    )

admin.site.register(Part, PartAdmin)


class ComponentInline(admin.TabularInline):
    model = Component
    # form = ComponentAdminForm
    # formset = ComponentInlineFormset
    extra = 1


# class ComponentAdmin(admin.ModelAdmin):
#
#     list_display = ['product', 'part', 'unit_quantity']
#     list_filter = (
#         'product__name',
#     )
# admin.site.register(Component, ComponentAdmin)


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ComponentInline,
    ]

    form = ProductAdminForm

    list_display = ['name', 'product_code', 'batch', 'packaging_warehouse', 'maximum_available']
    list_filter = (
        'name',
        'batch__number',
        'batch__expire_date',
        'packaging_warehouse',
    )
    search_fields = (
        'name',
        'product_code',
        'packaging_warehouse__name',
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


class PartOrderedAdmin(admin.ModelAdmin):
    list_display = ['part', 'ordered_item', 'quantity']
    list_filter = (
        'part',
        'ordered_item',
    )
    readonly_fields = ['part', 'ordered_item', 'quantity']


admin.site.register(PartOrdered, PartOrderedAdmin)


class OrderedItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'product', 'quantity']
    list_filter = (
        'order__order_name',
        'product',
        'order__client',
        'status',
    )
    search_fields = (
        'order__order_name',
        'product__name',
        'order__client',
        'status__name',
    )


admin.site.register(OrderedItem, OrderedItemAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderedItem
    extra = 1
    fields = ['product', 'status', 'quantity']
    readonly_fields = ['status']
    # form = InlineForm


    # def get_formset(self, request, obj=None, **kwargs):
    #     InlineForm.obj = obj
    #     return super(OrderItemInline, self).get_formset(request, obj, **kwargs)

        # return formset


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
    list_display = ['order_name', 'order_number', 'status', 'client', 'delivered_by']
    list_filter = (
        'status',
        'order_number',
        'client',
        'delivered_by'
    )
    # readonly_fields = ["status"]

    def save_formset(self, request, form, formset, change):
        create_status, _ = Status.objects.get_or_create(name="Created")
        order = Order.objects.get(order_number=formset.instance.order_number)
        if not order.status:
            formset.instance.status = create_status

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
        msgs = []
        for part, total_quantity_needed in parts_needed.items():
            if part.available < total_quantity_needed != 0:
                msgs.append(
                    f"Part name: [{part.name}, batch: {part.batch.number}] short: {total_quantity_needed - part.available} in {part.warehouse.name}")
                submit_order = False
        if submit_order:
            messages.info(
                request,
                f"{formset.instance.order_name} - [{formset.instance.order_number}] has been submittted."
            )
            # submitted, _ = Status.objects.get_or_create(name="Submitted")
            # if order.status.name != submitted.name:
            #     Order.objects.filter(order_number=order.order_number).update(status=submitted)
            #     for part, total_quantity_needed in parts_needed.items():
            #         part.available -= total_quantity_needed
            #         part.save()
            #         for component in Component.objects.filter(part=part):
            #             component.product.save()
        else:
            order.status = create_status
            order.save()
            messages.warning(request, f"Unable to submit order: [{formset.instance.order_number}]")
            for msg in msgs:
                messages.warning(request, msg)

        return super().save_formset(request, form, formset, change)
        # Revert an order
        # if order.status.name == "Cancelled":
            # for part, total_quantity_needed in parts_needed.items():
            #     part.available += total_quantity_needed
            #     part.save()





admin.site.register(Order, OrderAdmin)
