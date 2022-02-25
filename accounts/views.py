from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from cart.views import _cart_id
from orders.models import  Order, OrderProduct
import requests
from django.contrib.auth.decorators import user_passes_test
from store.models import Product

# Create your views here.
def login(request):
    
    if request.method == "POST":
        username       = request.POST["username"]
        password       = request.POST["password"]
        user = auth.authenticate(username= username, password = password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    id = []
                    for item in cart_item:
                        id.append(item.id)

                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
            #return redirect("index1")
        else:
            return redirect('login')
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        User_Name        = request.POST["username"]
        Email_ID         = request.POST["email"]
        Password         = request.POST["password"]
        Confirm_Password = request.POST["confirm_password"]
        if Password == Confirm_Password:
            if User.objects.filter(username = User_Name).exists():
                print("Username Taken")
            elif User.objects.filter(email = Email_ID).exists():
                print("Email Taken")
            else:
                user = User.objects.create_user(username= User_Name, password = Password , email= Email_ID)
                user.save()
                print("User Created")
                return render(request, "login.html")
        else:
            print('password not matching')
            return redirect("register")
    else:
        return render(request, "register.html")


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect("index1")


@login_required(login_url='login')
def dashboard(request):

    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    #userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        #'userprofile': userprofile,
    }
    return render(request, 'user_dashboard/dashboard_overview.html', context)


@login_required(login_url='login')
def invoice(request):
    return render(request, "user_dashboard/bill.html")


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, "user_dashboard/dashboard_my_orders.html", context)


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    # subtotal = 0
    # for i in order_detail:
    #     subtotal += i.product_price * i.quantity
    order_item_count = order_detail.count()
    context = {
        'order_detail': order_detail,
        'order': order,
        #'subtotal': subtotal,
        'order_item_count' :order_item_count
    }
    return render(request, 'user_dashboard/order_detail.html', context)

@login_required(login_url='login')
def my_rewards(request):

    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(request, "user_dashboard/dashboard_my_rewards.html", context)


@login_required(login_url='login')
def my_wallet(request):

    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    
    return render(request, "user_dashboard/dashboard_my_wallet.html", context)

@login_required(login_url='login')
def my_wishlist(request):

    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    
    return render(request, "user_dashboard/dashboard_my_wishlist.html", context)


@login_required(login_url='login')
def my_addresses(request):

    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    
    return render(request, "user_dashboard/dashboard_my_addresses.html", context)


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password= password)
        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                return redirect('admin_page')
            else:
                return redirect('admin_login')
        else:
            return redirect('admin_login')
    else:
        return render(request, 'admin_dashboard/login.html')


@user_passes_test(lambda u:u.is_superuser)
def admin_page(request):
    return render(request, "admin_dashboard/admin_dashboard.html")



@user_passes_test(lambda u:u.is_superuser)
def reports(request):
    return render(request, "admin_dashboard/reports.html")


@user_passes_test(lambda u:u.is_superuser)
def order_history(request):
    
    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, "admin_dashboard/order_history.html", context)


@user_passes_test(lambda u:u.is_superuser)
def customer(request):
    return render(request, "admin_dashboard/customer.html")


@user_passes_test(lambda u:u.is_superuser)
def invoice(request):
    
    # order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    # order = Order.objects.get(order_number=order_id)
    # order_item_count = order_detail.count()
    
    # context = {
    #     'order_detail': order_detail,
    #     'order': order,
    #     'order_item_count' :order_item_count
    # }
    
    return render(request, "admin_dashboard/invoice.html")


@user_passes_test(lambda u:u.is_superuser)
def products(request):
    
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products':products
    }
    return render(request, "admin_dashboard/Products.html", context)


@user_passes_test(lambda u:u.is_superuser)
def notifications(request):
    return render(request, "admin_dashboard/notifications.html")


@user_passes_test(lambda u:u.is_superuser)
def charts(request):
    labels = []
    data = []
    
    labels2 = []
    data2 = []
    
    
    queryset = Order.objects.order_by('-is_ordered')[:5]
    
    for order in queryset:
        labels.append(order.first_name)
        data.append(order.order_total)
        
            
    queryset2 = Product.objects.order_by('-is_available')[:5]
    
    for product in queryset2:
        labels2.append(product.product_name)
        data2.append(product.stock)
        
    print(labels)
    print(labels2)
    print(data)
    print(data2)
    return render(request, "charts_test.html",{
       
        'labels2': labels2,
        'data2': data2,
        'labels': labels,
        'data': data,
    })
    
