from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product,Category
from .models import Cart, Product, CartItem


def done(request):
    if not request.user.is_authenticated :
        return redirect('login') 

    return render(request,'success.html',{})


def checkout_view(request):
    if request.user.is_authenticated:
        # Get the user's cart
        cart = get_object_or_404(Cart, user_id=request.user)

        # Get all cart items
        cart_items = cart.cart_items.all()
        
        # Calculate total price
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        # Pass cart items and total price to the template
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        
        return render(request, 'checkout.html', context)
    else:
        # Redirect to login if the user is not authenticated
        return redirect('login') 


def view_cart(request):
    if not request.user.is_authenticated :
        return redirect('login') 
    cart, created = Cart.objects.get_or_create(user_id=request.user)  # Get or create the cart for the user
    cart_items = cart.cart_items.all()  # Fetch all cart items
    total_price = sum(item.quantity * item.product.price for item in cart_items)  # Calculate total price
    cart.total_price = total_price  # Update total price in the cart
    cart.save()

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease' and cart_item.quantity > 1:  # Prevent going below 1
            cart_item.quantity -= 1
            cart_item.save()
    
    return redirect('cart') 


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()  # Remove the cart item
    return redirect('cart') 

def add_to_cart(request, product_id, quantity=1):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user_id=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()
    update_total_price(cart)

    next_url = request.POST.get('next', 'home')  
    return redirect(next_url)





def update_total_price(cart):
    total = sum(item.product.price * item.quantity for item in cart.cart_items.all())
    cart.total_price = total
    cart.save()


# Create your views here.
def home(request):
    products  = Product.objects.all()
    return render(request,'home.html',{'products' : products})

def login_user(request):
    if request.method == 'POST':
        username  = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None :
            login(request,user)
            messages.success(request,("You successfully logged in!"))
            return redirect('home')
        else :
            messages.success(request,('Wrong credentials !'))
            return redirect('login')

    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("Successfully Logged Out!"))
    return redirect('home')


        
    
    
def reg(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        user1 = User.objects.create_user(username=username, email=email, password=password1)
        user1.save()
        messages.success(request, "Registration successful. You can now log in.")
        user = authenticate(username=username,password=password1)
        login(request,user)
        return redirect('home')
    else:
        return render(request,'register.html',{})
    
def product_detail(request, slug):
    if not request.user.is_authenticated :
        return redirect('login') 
    product = get_object_or_404(Product, slug=slug)
    cart_item_exists = False

    # Check if the user is authenticated and if the product is already in the cart
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user_id=request.user)
        cart_item_exists = CartItem.objects.filter(cart=cart, product=product).exists()

    return render(request, 'product_detail.html', {
        'product': product,
        'cart_item_exists': cart_item_exists
    })
        

def cat(request, slug):
    if not request.user.is_authenticated :
        return redirect('login') 
    # Get the category based on the slug
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)
    
    # Filter products based on the category
    products = Product.objects.filter(category=category)

    # Initialize an empty list for cart item product IDs
    cart_item_ids = []

    # If the user is authenticated, get the cart item product IDs
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user_id=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_item_ids = list(cart_items.values_list('product_id', flat=True))

    # Pass the category, products, and cart item IDs to the template
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'cart_item_ids': cart_item_ids
    }

    return render(request, 'category.html', context)
