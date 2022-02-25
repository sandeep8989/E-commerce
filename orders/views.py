from cart.views import cart
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from cart.models import CartItem, Cart
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from cart.views import _cart_id


# def payments(request):
#     body = json.loads(request.body)
#     order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

#     # Store transaction details inside Payment model
#     payment = Payment(
#         user = request.user,
#         payment_id = body['transID'],
#         payment_method = body['payment_method'],
#         amount_paid = order.order_total,
#         status = body['status'],
#     )
#     payment.save()

#     order.payment = payment
#     order.is_ordered = True
#     order.save()

#     # Move the cart items to Order Product table
#     cart_items = CartItem.objects.filter(user=request.user)

#     for item in cart_items:
#         orderproduct = OrderProduct()
#         orderproduct.order_id = order.id
#         orderproduct.payment = payment
#         orderproduct.user_id = request.user.id
#         orderproduct.product_id = item.product_id
#         orderproduct.quantity = item.quantity
#         orderproduct.product_price = item.product.price
#         orderproduct.ordered = True
#         orderproduct.save()

#         cart_item = CartItem.objects.get(id=item.id)
#         product_variation = cart_item.variations.all()
#         orderproduct = OrderProduct.objects.get(id=orderproduct.id)
#         orderproduct.variations.set(product_variation)
#         orderproduct.save()


#         # Reduce the quantity of the sold products
#         product = Product.objects.get(id=item.product_id)
#         product.stock -= item.quantity
#         product.save()

#     # Clear cart
#     CartItem.objects.filter(user=request.user).delete()

#     # Send order recieved email to customer
#     mail_subject = 'Thank you for your order!'
#     message = render_to_string('orders/order_recieved_email.html', {
#         'user': request.user,
#         'order': order,
#     })
#     to_email = request.user.email
#     send_email = EmailMessage(mail_subject, message, to=[to_email])
#     send_email.send()

#     # Send order number and transaction id back to sendData method via JsonResponse
#     data = {
#         'order_number': order.order_number,
#         'transID': payment.payment_id,
#     }
#     return JsonResponse(data)

def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('index1')

    grand_total = 0
    for cart_item in cart_items:
        total += (cart_item.product.product_selling_price * cart_item.quantity)
        quantity += cart_item.quantity
    grand_total = total 

    if request.method == 'POST':
        
            # Store all the billing information inside Order table
        user = current_user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone_no']
        email = request.POST['email']
        address = request.POST['address']
        post_code = request.POST['post_code']
        country = request.POST['country']
        city = request.POST['town_city']
        order_note = request.POST['order_note']
        order_total = grand_total
        ip = request.META.get('REMOTE_ADDR')


        data = Order.objects.create(user=user,first_name=first_name, last_name=last_name,phone=phone, 
        email=email, address=address, post_code=post_code,country=country,city=city,order_note=order_note,
        order_total=order_total,ip=ip)
        data.save()
    
        # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        order_number = current_date + str(data.id)
        order_number = order_number
        
        data.order_number=order_number
        data.save()

        if request.user.is_authenticated:
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            #order_count = cart_item.count()
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'grand_total': grand_total,
                'item_count': cart_count,
                'date' : current_date,

            }
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            order = Order.objects.get(cart=cart, is_ordered=False, order_number=order_number)
            #order_count = order.count()
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'grand_total': grand_total,
            }

        # Move the cart items to Order Product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            # orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.product_selling_price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()


        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

        # Send order recieved email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('order_recieved_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        # send_email.attach_alternative(message, "text/html")
        # pdf = render_to_pdf('some_invoice.html')
        # send_email.attach('invoice.pdf', pdf)
        send_email.send()

        data.is_ordered = True
        data.save()

        return render(request, 'bill.html', context)
        #return redirect('invoice', context)

    else:
        return redirect('place_order')

# def order_complete(request):
#     order_number = request.GET.get('order_number')
#     transID = request.GET.get('payment_id')

#     try:
#         order = Order.objects.get(order_number=order_number, is_ordered=True)
#         ordered_products = OrderProduct.objects.filter(order_id=order.id)

#         subtotal = 0
#         for i in ordered_products:
#             subtotal += i.product_price * i.quantity

#         payment = Payment.objects.get(payment_id=transID)

#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'order_number': order.order_number,
#             'transID': payment.payment_id,
#             'payment': payment,
#             'subtotal': subtotal,
#         }
#         return render(request, 'orders/order_complete.html', context)
#     except (Payment.DoesNotExist, Order.DoesNotExist):
#         return redirect('home')