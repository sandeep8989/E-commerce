from django.urls import path
from store import views 

urlpatterns = [
    path('', views.home1, name ="home1"),
    path('index2', views.index2, name = "index2"),
    path('index1', views.index1, name ="index1"),
    path('fruits', views.fruits, name="fruits"),
    path('grocery', views.grocery, name="grocery"),
    path('pulses', views.pulses, name="pulses"),
    path('spices', views.spices, name="spices"),
    path('vegetables', views.vegetables, name="vegetables"),
    path('product/<int:product_id>/', views.shop_detail_fullwidth2, name="shop_detail_fullwidth2"),
    path('shop_wishlist/<int:product_id>/', views.shop_wishlist, name="shop_wishlist"),
    path("shop_compare", views.shop_compare, name="shop_compare"), 
    path('contact_us', views.contact_us, name="contact_us"),
    path('about_us', views.about_us , name="about_us"),
    path('search/', views.search, name='search'),
]