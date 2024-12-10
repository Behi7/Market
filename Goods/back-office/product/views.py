from Goods import models
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

def listProduct(request):
    queryset = models.Product.objects.all()
    context = {}
    paginator = Paginator(queryset, 1)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context['products'] = products
    return render(request, 'back-office/product/list.html',context)

def detailProduct(request, slugCategory, slugsubcategory, slugproduct):
    product = models.Product.objects.get(slug=slugproduct)
    recommendations_product = models.Product.objects.filter(subcategory=product.subcategory).exclude(id=product.id)
    if len(recommendations_product) > 4:
        recommendations_product = random.sample(list(recommendations_product), 3)
    context = {}
    context['product'] = product
    context['images'] = models.ProductImg.objects.filter(product = product)
    context['recommendations_product'] = recommendations_product
    return render(request, 'back-office/product/product-details.html', context)

def productlists(request):
    products = models.Product.objects.all()
    context = {}
    try:
        wishProducts = models.WishList.objects.filter(user = request.user)
        for wish in wishProducts:
            for product in products:
                if wish.product.id == product.id:
                    product.is_active = True
    except:
        ...
    products = models.Product.objects.all()
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context['products'] = products
    categories = models.Category.objects.all()
    context['categorys'] = categories
    return render(request, 'shop.html', context)

def categorysubcategorylisyt(request, slugCategory, slugsubcategory):
    subcategory = models.SubCategory.objects.get(slug = slugsubcategory)
    product = subcategory.productlist
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'shop.html', {'products': product, 'categorys':categories})

def categoryProductlist(request, slugCategory):
    category = models.Category.objects.get(
        slug = slugCategory
        )
    subcategories = category.subcategorieslist
    allproduct = models.Product.objects.all()
    product = []
    for subcategory in subcategories:
        for productfilter in allproduct:
            if productfilter.subcategory == subcategory:
                product.append(productfilter)
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'shop.html', {'products': product, 'categorys':categories})

def addProductToCart(request, id):
    product = models.Product.objects.get(id=id)
    cart, _ = models.Cart.objects.get_or_create(author=request.user, is_active=True)
    try:
        cart_product = models.CartProduct.objects.get(cart=cart.id, product=product.id)
        cart_product.quantity+=request.POST['quantity']
        cart_product.save()
    except:
        cart_product = models.CartProduct.objects.create(
            product=product, 
            cart=cart,
            quantity=request.POST['quantity']
        )
    return redirect(request.META.get('HTTP_REFERER'))

