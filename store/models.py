from django.db import models
from django.db.models.fields import BooleanField, CharField, DateField, IntegerField, SlugField, TextField
from django.db.models.fields.files import ImageField

# Create your models here.


class Product(models.Model):
    product_image           = ImageField(upload_to='products/pics') 
    product_name            = CharField(max_length=20, unique=True)
    product_type            = CharField(max_length=20)
    slug                    = SlugField(max_length=20,unique=True)
    product_description     = TextField(max_length=500, blank=True)
    product_selling_price   = IntegerField()
    product_orginal_price   = IntegerField()
    stock                   = IntegerField()
    is_available            = BooleanField(default=True)
    created_date            = DateField(auto_now_add=True)
    modified_date           = DateField(auto_now=True)


    def __str__(self):
        return self.product_name

