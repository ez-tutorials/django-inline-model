from django.contrib import admin

# Register your models here.
from .models import Group, Membership, Person
from .models import Role, Movie, Artist
from .models import Book, Author
from .models import Part, Product, Warehouse, Component

from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter




class CustomModelAdmin(object):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != 'id'
        ]
        super(CustomModelAdmin, self).__init__(model, admin_site)


@admin.register(Group)
class GroupAdmin(CustomModelAdmin, admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(CustomModelAdmin, admin.ModelAdmin):
    pass


@admin.register(Membership)
class MembershipAdmin(CustomModelAdmin, admin.ModelAdmin):
    pass


class RoleInline(admin.TabularInline):
    model = Role
    extra = 1


class ArtistAdmin(admin.ModelAdmin):
    inlines = (RoleInline,)


class MovieAdmin(admin.ModelAdmin):
    inlines = (RoleInline,)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Role)


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline,
    ]
admin.site.register(Author, AuthorAdmin)


class PartAdmin(admin.ModelAdmin):
    pass
admin.site.register(Part, PartAdmin)


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1
    # list_field = ['part', 'warehouse', 'quantity']

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "warehouse":
    #         kwargs["queryset"] = Part.objects.filter(warehouse=db_field.value)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        return super().formfield_for_choice_field(db_field, request, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ComponentInline,
    ]

admin.site.register(Product, ProductAdmin)


class WarehouseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Warehouse, WarehouseAdmin)


