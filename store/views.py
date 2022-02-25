from django.shortcuts import render
from .models import Product
from django.db.models import Q

# Create your views here.
def index2(request):
    
    return render(request ,"store/index.html")

def index1(request):

    products = Product.objects.all().filter(is_available=True)
    
    return render(request, "store/milk.html", {'products':products})

def home(request):
    return render(request, "store/home.html")

def home1(request):
    return render(request, "store/home1.html")

def grocery(request):

    products = Product.objects.all()

    return render(request, "store/grocery.html",{'products':products})

def fruits(request):

    products = Product.objects.all()

    return render(request, "store/fruits.html",{'products':products})

def pulses(request):

    products = Product.objects.all()

    return render(request, "store/pulses.html",{'products':products})

def spices(request):

    products = Product.objects.all()

    return render(request, "store/spices.html", {'products':products})

def vegetables(request):

    products = Product.objects.all()

    return render(request, "store/vegetables.html",{'products':products})

def shop_detail_fullwidth2(request,product_id):

    products = Product.objects.all().filter(is_available=True)

    product = Product.objects.get(id=product_id)

    return render(request, "store/shop_detail_fullwidth2.html", {"product" : product, "products":products})

def shop_wishlist(request,product_id):

    product = Product.objects.get(id=product_id)

    print(product)
    return render(request, "store/shop_wishlist.html", {"product": product}) 

def shop_compare(request):

    return render(request, "store/shop_compare.html")

def about_us(request):
    return render(request, "store/about_us.html")

def contact_us(request):
    return render(request, "store/contact_us.html")


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/search.html',context)
