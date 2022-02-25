from django.contrib import admin

# Register your models here.
from store.models import Product
from orders.models import Order, OrderProduct


class PostAdminSite(admin.AdminSite):
    site_header = "Vender Login"
    site_title = "Vender home Page"
    index_title = "Welcome to Vendor Page"

post_admin_site = PostAdminSite(name='vendor')


post_admin_site.register(Product)
post_admin_site.register(Order)
post_admin_site.register(OrderProduct)