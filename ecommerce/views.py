import json
import datetime
from .utils import *
from .models import *
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login # Rename the import to avoid the conflict
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# Create your views here.

@csrf_exempt
def login(request):
    context = {}
    if request.method == "POST":
        identifier = request.POST.get('identifier')  # this will serve as either username, email or phone number
        password = request.POST.get('password')
        
        # Check against username, email, and phone number fields in the Customer model
        try:
            # Since username and email fields are unique, you can use 'get' safely.
            # For phone numbers, make sure it's unique or use a filter and get the first result.
            customer = Customer.objects.filter(
                Q(username=identifier) | Q(email=identifier) | Q(phone_number=identifier)
            ).first()

            if customer:
                user = authenticate(request, username=customer.username, password=customer.password)
                if user is not None:
                    user_login(request, user)
                    return redirect('store')  # Redirect to desired URL after login
                else:
                    context['error'] = "Invalid password."
            else:
                context['error'] = "No account associated with this identifier."

        except Customer.DoesNotExist:
            context['error'] = "No account found."

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
                    # user = User.objects.create_user(username=username, email=email, password=password)

                    # Create a Customer instance after creating the User
                    Customer.objects.create(
                        # user=user,
                        username=username,
                        email=email,
                        phone_number=phone_number,
                        password=password  # Storing raw passwords is not secure; consider hashing.
                    )

                    return redirect('login')  # Redirect to desired URL after registration
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