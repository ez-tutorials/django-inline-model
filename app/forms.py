from django import forms
from django.db.models import ManyToManyRel
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, ManyToManyRawIdWidget
from django.utils.translation import ugettext_lazy as _
from app.models import *


class CountryForm(forms.Form):
    OPTIONS = (
        ("AUT", "Austria"),
        ("DEU", "Germany"),
        ("NLD", "Neitherlands"),
    )
    Countries = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=OPTIONS
    )


class SupplierAdminForm(forms.ModelForm):

    # When this field is enabled, it's required
    # address = forms.CharField(help_text="Supplier's address")
    class Meta:
        model = Supplier
        exclude = []

    def clean_address(self):
        address = self.cleaned_data.get("address")
        if not address:
            # raise ValidationError(_('Invalid address'))
            address = "Updated in form"
        return address


class ProductAdminForm(forms.ModelForm):

    # When this field is enabled, it's required
    name = forms.CharField(help_text="Product name.")
    # batch = forms.ModelChoiceField(
    #     Batch.objects.all(),
    #     help_text="Give the product a batch number."
    # )
    # packaging_warehouse = forms.CharField(help_text="Where the product is being packaged.")

    class Meta:
        model = Product
        exclude = []




    # def cleaned_data(self):
