from django.db import models

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






class Part(models.Model):
    name = models.CharField(max_length=100)


class Component(models.Model):
    name = models.CharField(max_length=100)
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING)
    part_quantity = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    component = models.ManyToManyField(Component, related_name='component')



