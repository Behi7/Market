from django.shortcuts import render, redirect
from Goods import models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='register')
def myCart(request):
    cart, _ = models.Cart.objects.get_or_create(
        author=request.user, 
        is_active=True)
    context = {}
    cart_products = models.CartProduct.objects.filter(cart = cart)
    totalcart = 0
    for product in cart_products:
        totalcart += product.total
    context['totalcart'] = totalcart
    context['cart']=cart
    # context['cart_products'] = cart_products
    paginator = Paginator(cart_products, 1)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context['cart_products'] = products
    return render(request, 'back-office/user/cart.html', context)

@login_required(login_url='register')
def addProductToCart(request, id):
    product = models.Product.objects.get(id=id)
    cart, _ = models.Cart.objects.get_or_create(author=request.user, is_active=True)
    try:
        cart_product = models.CartProduct.objects.get(cart=cart.id, product=product.id)
        cart_product.save()
    except:
        cart_product = models.CartProduct.objects.create(
            product=product, 
            cart=cart
        )
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='register')
def substractProductFromCart(request, id):
    print(request)
    quantity = request.GET['quantity']
    product_cart = models.CartProduct.objects.get(id=id)
    product_cart.quantity -= quantity
    product_cart.save()
    if not product_cart.quantity:
        product_cart.delete()
    return redirect('/')

@login_required(login_url='register')
def plusOrMinusCart(request, id, sign):
    try:
        cartproduct = models.CartProduct.objects.get(id=id)
    except models.CartProduct.DoesNotExist:
        return redirect('cart')

    if sign == 'plus':
        cartproduct.quantity += 1
    elif sign == 'minus':
        if cartproduct.quantity > 1:
            cartproduct.quantity -= 1
        else:
            cartproduct.delete()
    models.CartProduct.objects.filter(id=id).update(quantity=cartproduct.quantity)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='register')
def deleteProductCart(request, id):
    product_cart = models.CartProduct.objects.get(id=id)
    product_cart.delete()
    return redirect('myCart')

@login_required(login_url='register')
def fullDeleteCart(request):
    cart = models.Cart.objects.get(author = request.user).delete()
    return redirect('myCart')

@login_required(login_url='register')
def createOrder(request):
    cart = models.Cart.objects.get(
        author = request.user
        )
    cart_products = models.CartProduct.objects.filter(cart=cart)

    done_products = []
    print(f'---------------{request.POST}')
    for cart_product in cart_products:
        if cart_product.quantity <= cart_product.product.quantity:
            cart_product.product.quantity -= cart_product.quantity
            cart_product.product.save()
            done_products.append(cart_product)   
        else:
            for product in done_products:
                product.product.quantity += product.quantity
                product.product.save()
            raise ValueError('нехватает товара')
        models.Order.objects.create(
            cart=cart,
            full_name = f"{request.user.first_name}, {request.user.last_name}",
            email = request.user.email,
            phone = request.POST['phone'],
            address = request.POST['address'],
            status = 1
            )
        cart.is_active = False
        cart.save()
    cart.delete() 
    return redirect('/')

@login_required(login_url='register')
def fullDeleteCart(request):
    models.Cart.objects.get(author=request.user).delete()
    return redirect('myCart')

