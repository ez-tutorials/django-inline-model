from django.db import models
from smart_selects.db_fields import GroupedForeignKey, ChainedForeignKey

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=50)


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('group', 'person'),
    )


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)


class Artist(models.Model):
    name = models.CharField(max_length=200)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    artists = models.ManyToManyField(Artist, related_name='actor')


class Role(models.Model):
    role_name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)





class Author(models.Model):
   name = models.CharField(max_length=100)

class Book(models.Model):
   author = models.ForeignKey(Author, on_delete=models.CASCADE)
   title = models.CharField(max_length=100)


class Warehouse(models.Model):
   name = models.CharField(max_length=100)

   def __str__(self):
       return f"{self.name}"


class Product(models.Model):
   name = models.CharField(max_length=100)

   def __str__(self):
       return f"{self.name}"


class Part(models.Model):
    name = models.CharField(max_length=100)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} in {self.warehouse}"


class Component(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse')
    # grouped_part = GroupedForeignKey(Part, 'warehouse')
    part = ChainedForeignKey(
        Part,
        chained_field="warehouse",
        chained_model_field="warehouse",
        show_all=True,
        auto_choose=True,
        sort=True
    )
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product} in {self.warehouse}"


