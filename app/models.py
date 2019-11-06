from django.db import models
from smart_selects.db_fields import GroupedForeignKey, ChainedForeignKey

# Create your models here.


#
#
# class Group(models.Model):
#     name = models.CharField(max_length=128)
#     members = models.ManyToManyField(
#         Person,
#         through='Membership',
#         through_fields=('group', 'person'),
#     )
#
#
# class Membership(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
#     inviter = models.ForeignKey(
#         Person,
#         on_delete=models.CASCADE,
#         related_name="membership_invites",
#     )
#     invite_reason = models.CharField(max_length=64)
#
#
# class Artist(models.Model):
#     name = models.CharField(max_length=200)
#
#
# class Movie(models.Model):
#     title = models.CharField(max_length=100)
#     artists = models.ManyToManyField(Artist, related_name='actor')
#
#
# class Role(models.Model):
#     role_name = models.CharField(max_length=100)
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#
#
#
#
#
# class Author(models.Model):
#    name = models.CharField(max_length=100)
#
# class Book(models.Model):
#    author = models.ForeignKey(Author, on_delete=models.CASCADE)
#    title = models.CharField(max_length=100)


class Person(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Status(models.Model):
    # Available, Delivered, Ordered
    name = models.CharField(max_length=255, default='Available')

    def __str__(self):
        return f"{self.name}"


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Client(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.ForeignKey(
        Person, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}"


class Batch(models.Model):
    number = models.CharField(max_length=255)
    manufacture_date = models.DateField()
    expire_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.number} from {self.supplier.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Part(models.Model):
    name = models.CharField(max_length=255)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    available_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.batch.number} stored in " \
               f"{self.warehouse}, {self.available_total} available."


class Component(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    # warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, related_name='warehouse')
    part = GroupedForeignKey(Part, 'warehouse')
    # batch = GroupedForeignKey(Batch, 'supplier')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        part_names = []
        if self.part:
            p_name = Part.objects.get(id=self.part.id).name
            part_names.append(p_name)
        return f"{self.product.name}: {part_names}"


# Order model on save()
#   Based on Product and its part, update the

class Order(models.Model):
    order_name = models.CharField(max_length=255, default="Order")
    delivered_by = models.DateField(blank=True, null=True)

    def __str__(self):
        product_list = []
        # if self.product:
        return f"{self.order_name}"


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    # product = GroupedForeignKey(Product, "status")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        product_names = []
        if self.product:
            p_name = Product.objects.get(id=self.product.id).name
            product_names.append(p_name)
        return f"{product_names} - {self.quantity}"

