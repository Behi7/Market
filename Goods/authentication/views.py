from django.shortcuts import render
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q 

def main(request):
    context = {}
    products = models.Product.objects.all()
    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context['products'] = products
    context['products'] = products
    context['banners']= models.Banner.objects.filter(is_active = True)[:5]
    context['info'] = models.Info.objects.last()
    try:
        wishProducts = models.WishList.objects.filter(user = request.user)
        for wish in wishProducts:
            for product in products:
                if wish.product.id == product.id:
                    product.is_active = True
    except:
        ...
    categories = models.Category.objects.all()
    context['categorys'] = categories
    return render(request, 'index.html', context)

def search(request):
    query = ""
    results = []
    if request.method == "POST":
        results = models.Product.objects.filter(name__icontains=request.POST['search'])
    return render(request, 'shop.html', {'products': results, 'query': query})
