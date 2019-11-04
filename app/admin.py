from django.contrib import admin

# Register your models here.
from .models import Group, Membership, Person
from .models import Role, Movie, Artist
from .models import Component, Product, Part

from django.contrib import admin


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


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (ComponentInline,)


class PartAdmin(admin.ModelAdmin):
    inlines = (ComponentInline,)


admin.site.register(Product, ProductAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Component)
