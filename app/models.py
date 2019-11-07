import uuid
from django.db import models
from django.contrib import messages
from django_extensions.db.models import TimeStampedModel

from smart_selects.db_fields import GroupedForeignKey, ChainedForeignKey


class Person(TimeStampedModel, models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Status(TimeStampedModel, models.Model):
    # Available, Delivered, Ordered
    name = models.CharField(max_length=255, default='Available')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Statuses"


class Warehouse(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Client(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Supplier(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.ForeignKey(
        Person, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}"


class Batch(TimeStampedModel, models.Model):
    number = models.UUIDField(default=str(uuid.uuid4()), unique=True)
    manufacture_date = models.DateField()
    manufacture_place = models.CharField(
        max_length=255,
        default='Cape Town, South Africa'
    )
    expire_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.number} from {self.supplier.name}"

    class Meta:
        verbose_name_plural = "Batches"


class Product(TimeStampedModel, models.Model):
    name = models.CharField(max_length=100)
    product_code = models.UUIDField(default=str(uuid.uuid4()))
    batch = models.ForeignKey(
        Batch,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    packaging_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # This is worked out from current available parts in the warehouse
    maximum_available = models.IntegerField(default=0)

    class Meta:
        unique_together = [
            'product_code',
            'batch'
        ]

    def __str__(self):
        return f"{self.name}, available max: {self.maximum_available} in {self.packaging_warehouse}"

    def save(self, *args, **kwargs):
        max_avail = 999999
        for cp in Component.objects.filter(product=self.id):
            if cp.part.warehouse == self.packaging_warehouse:
                if cp.part.available_total / cp.unit_quantity < max_avail:
                    max_avail = cp.part.available_total / cp.unit_quantity
        if max_avail != 999999:
            self.maximum_available = max_avail
        else:
            self.maximum_available = 0
        super(Product, self).save(*args, **kwargs)


class Part(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    part_code = models.UUIDField(default=str(uuid.uuid4()))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    available_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} [{self.batch.number}] stored in " \
               f"{self.warehouse}, {self.available_total} available."

    class Meta:
        unique_together = [
            'part_code',
            'batch'
        ]


class Component(TimeStampedModel, models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    part = GroupedForeignKey(Part, 'warehouse')
    unit_quantity = models.IntegerField(default=0)

    class Meta:
        ordering = ['-product__name']

    def __str__(self):
        part_names = []
        if self.part:
            p_name = Part.objects.get(id=self.part.id).name
            part_names.append(p_name)
        return f"{self.product.name}: {part_names}"

    def save(self, *args, **kwargs):
        # only save the component if unit_quantity is greater than 0
        if self.unit_quantity > 0 and self.part:
            super(Component, self).save(*args, **kwargs)
            self.product.save()

    def delete(self, *args, **kwargs):
        super(Component, self).delete()
        self.product.save()


class Order(TimeStampedModel, models.Model):
    order_name = models.CharField(max_length=255, default="Order")
    order_number = models.UUIDField(default=str(uuid.uuid4()))
    delivered_by = models.DateField(blank=True, null=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = [
            'order_name',
            'order_number',
            'client'
        ]

    def __str__(self):
        client_msg = f" to {self.client}" if self.client else ""
        return f"{self.order_name}"

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Order, self).delete()


class OrderedItem(TimeStampedModel, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = GroupedForeignKey(Product, "batch")
    quantity = models.IntegerField(default=0)

    class Meta:
        ordering = [
            'product__name'
        ]
        unique_together = [
            'product',
            'order'
        ]

    def __init__(self, *args, **kwargs):
        super(OrderedItem, self).__init__(*args, **kwargs)
        self._initial_data = self.__dict__.copy()

    def __str__(self):
        product_names = []
        if self.product:
            p_name = Product.objects.get(id=self.product.id).name
            product_names.append(p_name)
        return f"{product_names} - {self.quantity}"

    def save(self, *args, **kwargs):
        changed = {
            k: self.__dict__[k] for k, v in self._initial_data.items()
            if v != self.__dict__[k] and k not in ('log', 'activity', '_state',)
        }

        if self.quantity > 0 and self.product:
            super(OrderedItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # messages.add_message(request, messages.ERROR, 'Car has been sold')
        super(OrderedItem, self).delete()
