from Goods import models
from django.shortcuts import render, redirect


def createBanner(request):
    if request.method == 'POST':
        create = models.Banner.objects.create(
            title = request.POST['title'],
            sub_title = request.POST['sub_title'],
            images = request.FILES['images'],
        )
    return render(request, 'banner/createbanner.html')

def listBanner(request):
    context = {}
    context['banners'] = models.Banner.objects.all()
    return render(request, 'banner/list.html', context)

def deleteBanner(request, id):
    models.Banner.objects.get(id=id).delete()
    return redirect('list')