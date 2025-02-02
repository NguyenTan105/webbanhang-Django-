from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


# def register(request):
#     form = CreateUserForm()
#     if request.method == "POST":
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#     context = {'form': form}
#     return render(request, 'app/register.html', context)
def detail(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "none"
        user_login = "inline"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "inline"
        user_login = "none"
    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)
    context = {'items': items, 'cartItems': cartItems, 'products': products,
               'user_not_login': user_not_login, 'user_login': user_login, 'categories': categories, 'active_category': active_category}
    return render(request, 'app/detail.html', context)


def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "none"
        user_login = "inline"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "inline"
        user_login = "none"
    context = {'products': products, 'cartItems': cartItems,
               'user_not_login': user_not_login, 'user_login': user_login, 'categories': categories, 'active_category': active_category}
    return render(request, 'app/category.html', context)


def search(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    if request.method == "POST":
        searched = request.POST['searched']
        keys = Product.objects.filter(name__contains=searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "none"
        user_login = "inline"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "inline"
        user_login = "none"
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems,
               'searched': searched, 'keys': keys, 'user_not_login': user_not_login, 'user_login': user_login, 'categories': categories, 'active_category': active_category}
    return render(request, 'app/search.html', context)


def register(request):
    if request.method == "POST":
        # Lấy dữ liệu từ request.POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Kiểm tra xem username đã tồn tại hay chưa
        if User.objects.filter(username=username).exists():
            messages.error(
                request, 'Username đã tồn tại, vui lòng chọn username khác.')
            return redirect('register')

        # Kiểm tra xác nhận mật khẩu
        if password1 != password2:
            messages.error(
                request, 'Mật khẩu và xác nhận mật khẩu không khớp.')
            return redirect('register')

        # Tạo người dùng mới
        user = User.objects.create_user(
            username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        user.save()

        messages.success(request, 'Đăng ký thành công!')
        return redirect('login')

    return render(request, 'app/register.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'user or password not correct!')
    context = {}
    return render(request, 'app/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def get_home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "none"
        user_login = "inline"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "inline"
        user_login = "none"
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems,
               'user_not_login': user_not_login, 'user_login': user_login, 'categories': categories, 'active_category': active_category}
    return render(request, 'app/home.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "none"
        user_login = "inline"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "inline"
        user_login = "none"
    categories = Category.objects.filter(is_sub=False)
    context = {'items': items, 'order': order, 'cartItems': cartItems,
               'user_not_login': user_not_login, 'user_login': user_login, 'categories': categories}
    return render(request, 'app/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "none"
        user_login = "inline"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "inline"
        user_login = "none"
    context = {'items': items, 'order': order, 'cartItems': cartItems,
               'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # quantity = data['quantity']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    # elif action == 'add-quantity':
    #     orderItem.quantity += quantity
    orderItem.save()
    if orderItem.quantity == 0:
        orderItem.delete()
    if action == 'delete':
        orderItem.delete()

    return JsonResponse('added', safe=False)


def updateQuantity(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data['quantity']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add-quantity':
        orderItem.quantity += quantity
    orderItem.save()

    return JsonResponse('added', safe=False)
