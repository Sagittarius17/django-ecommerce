import json
import datetime
from .utils import *
from .models import *
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login   # Rename the import to avoid the conflict
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use the renamed import
            return HttpResponseRedirect('/')
    context = {}
    return render(request, 'ecommerce/login.html', context)

@csrf_exempt
def register(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([username, email, phone_number, password, confirm_password]):
            context['error'] = "Please fill all the fields."
        elif password != confirm_password:
            context['error'] = "Passwords do not match."
        else:
            try:
                if User.objects.filter(email=email).exists():
                    context['error'] = "Email already in use."
                elif User.objects.filter(username=username).exists():
                    context['error'] = "Username already in use."
                else:
                    # Note: Django's User model doesn't have a phone_number field by default.
                    # If you've customized the User model to have one, this will work.
                    # Otherwise, you'd need to handle phone_number separately.
                    user = User.objects.create_user(username=username, email=email, password=password)
                    # Assume you save the phone_number in user profile or another related model
                    user.phone_number = phone_number  
                    user.save()
                    return redirect('store')  # Redirect to desired URL after registration
            except Exception as e:
                context['error'] = str(e)  # Display the error message to the context

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
        
    else:
        customer, order = guestOrder(request, data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        order.complete = True
    order.save()  
      
    if order.shipping == True:
        ShippingAddress.objects.create (
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )
    
    return JsonResponse('Payment complete', safe=False)