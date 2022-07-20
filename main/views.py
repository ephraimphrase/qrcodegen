from django.shortcuts import render,redirect
from .models import Product
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
import uuid

# Create your views here.
def qrCodeGen(request):
    title = "QR generator"
    context = {'title':title}

    if request.method == "POST":
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = request.POST['price']
        description = request.POST['description']
        product_image = request.FILES['product_image']

        product = Product.objects.create(owner=request.user, name=name, quantity=quantity, price=price, description=description, product_image=product_image)
        product.save()

        return redirect('home')

    return render(request, 'qrCode.html', context)

def home(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
 
    title = 'Home'
    count = Product.objects.all().count()

    page_range = ''

    if request.GET.get('page_range'):
        page_range = request.GET.get('page_range')

    vert_count = Product.objects.filter(product_status=True).count()
    verf_count = Product.objects.filter(product_status=False).count()
    products = Product.objects.filter(Q(name__icontains=search_query) | Q(price__icontains=search_query) | Q(description__icontains=search_query), owner=request.user)
    paginator = Paginator(products, int(page_range, 10))
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_number = 1
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_number = paginator.num_pages
        page_obj = paginator.get_page(page_number)

    context = {'title':title, 'products':products, 'page_obj':page_obj, 'paginator':paginator, 'count':count, 'vert_count':vert_count, 'verf_count':verf_count }
    return render(request, 'home.html', context)

def signUp(request):
    if request.method == "GET":
        title = 'Register'
        context = {'title':title}
        return render(request, 'signup.html', context)

    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.save()

        login(request, user)
        return redirect('home')

def signIn(request):
    if request.method == "GET":
        title = 'Log In'
        context = {'title':title}
        return render(request, 'signin.html', context)

    else:
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password')
    
    return render(request, 'signin.html')

def signOut(request):
    logout(request)
    return redirect('signIn')

def landing(request):
    title = 'Landing Page'
    context = {'title':title}
    return render(request, 'landing.html', context)

def productInfo(request, pk):
    title = 'Product Info'
    product = Product.objects.get(id=pk)
    product.product_status = True
    product.save()
    context = {'title':title, 'product':product}
    return render(request, 'productInfo.html', context)

def scanner(request):
    title = 'Scanner'
    product = Product.objects.all()
    context = {'title':title, 'product':product}
    return render(request, 'scanner.html', context)