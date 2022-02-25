from django.urls import path
from accounts import views 

urlpatterns = [
    path('login', views.login, name = "login"),
    path('register', views.register, name= "register"),
    path('logout', views.logout, name='logout'), 
    path('dashboard', views.dashboard, name='dashboard'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my_rewards', views.my_rewards, name='my_rewards'),
    path('my_wallet', views.my_wallet, name='my_wallet'),
    path('my_wishlist', views.my_wishlist, name='my_wishlist'),
    path('my_addresses', views.my_addresses, name='my_addresses'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_page', views.admin_page, name='admin_page'),
    path('charts', views.charts, name='charts'),
    path('reports', views.reports, name='reports'),
    path('order_history', views.order_history, name='order_history'),
    path('customer', views.customer, name='customer'),
    path('invoice', views.invoice, name='invoice'),
    path('products', views.products, name='products'),
    path('notifications', views.notifications, name='notifications'),
]