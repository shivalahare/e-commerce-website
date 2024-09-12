from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login
from .models import Product, Cart, CartItem ,Order
from django.conf import settings
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, CartItem
from .forms import OrderForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'shop/Index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'item_id' in request.POST and 'quantity' in request.POST:
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity'))
            try:
                cart_item = CartItem.objects.get(id=item_id, cart=cart)
                cart_item.quantity = quantity
                cart_item.save()
                
                # Calculate updated item total and cart total
                item_total_price = cart_item.get_total_price()
                cart_total_price = sum(item.get_total_price() for item in cart.items.all())
                
                # Return updated prices as JSON
                return JsonResponse({
                    'item_total_price': float(item_total_price),
                    'cart_total_price': float(cart_total_price)
                })
            except CartItem.DoesNotExist:
                return JsonResponse({'error': 'Cart item not found'}, status=404)

        elif 'checkout' in request.POST:
            # Redirect to the checkout view
            return redirect('checkout')

    else:
        # Handle GET request
        items = CartItem.objects.filter(cart=cart)
        cart_total_price = sum(item.get_total_price() for item in items)
        context = {
            'items': items,
            'cart_total_price': cart_total_price
        }
        return render(request, 'shop/cart_detail.html', context)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


@login_required
def checkout(request):
    try:
        # Get the current user's cart
        cart = Cart.objects.get(user=request.user)
        
        if request.method == 'POST':
            # Iterate over each item in the cart to create orders
            for item in cart.items.all():
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.get_total_price(),
                    status='Pending'
                )
            
            # Optionally, clear the cart after successful order creation
            cart.items.all().delete()

            return redirect('order_success')  # Redirect to a success page or order summary
        
        # Calculate the total price for the cart
        total_price = sum(item.get_total_price() for item in cart.items.all())

        return render(request, 'shop/checkout.html', {'cart': cart, 'total_price': total_price})
    
    except Cart.DoesNotExist:
        return render(request, 'shop/checkout.html', {'error': 'Cart is empty.'})


def order_success(request):
    return render(request, 'shop/order_success.html')

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        response = request.POST
        params_dict = {
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_signature': response['razorpay_signature']
        }

        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            client.utility.verify_payment_signature(params_dict)

            # Update the order
            order = Order.objects.get(razorpay_order_id=params_dict['razorpay_order_id'])
            order.razorpay_payment_id = params_dict['razorpay_payment_id']
            order.razorpay_signature = params_dict['razorpay_signature']
            order.status = 'Completed'
            order.save()

            return render(request, 'payment_success.html')

        except:
            order = Order.objects.get(razorpay_order_id=params_dict['razorpay_order_id'])
            order.status = 'Failed'
            order.save()

            return render(request, 'payment_failed.html')

    return redirect('checkout')


