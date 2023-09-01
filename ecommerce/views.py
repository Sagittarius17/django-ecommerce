from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
from .utils import cookieCart, cookieData

# Create your views here.)

def login(request):
    context = {}
    return render(request, 'ecommerce/login.html', context)

def register(request):
    context = {}
    return render(request, 'ecommerce/register.html', context)

def store(request):
    data = cookieCart(request)
    cartItems = data['cartItems']
        
    products = Product.objects.all()
    context = {"products": products, 'cartItems': cartItems}
    return render(request, 'ecommerce/store.html', context)

@csrf_exempt
def cart(request):
    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {"items": items, 'order': order, 'cartItems': cartItems}
    return render(request, 'ecommerce/cart.html', context)

def checkout(request):
    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {"items": items, 'order': order, 'cartItems': cartItems}
    return render(request, 'ecommerce/checkout.html', context)

@csrf_exempt
def updateItem(request):
    try:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('product id:', productId)
        print('action:', action)
        
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
        
        orderItem.save()
        
        if orderItem.quantity == 0:
            orderItem.delete()
            
        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
    
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.object.create (
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            )
        
    else:
        print('user is not logged in')
    return JsonResponse('Payment complete', safe=False)