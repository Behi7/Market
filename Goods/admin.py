from django.contrib import admin
from . import models

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(models.Category, PostAdmin)
admin.site.register(models.SubCategory, PostAdmin)
admin.site.register(models.Product, PostAdmin)
admin.site.register(models.ProductImg)
admin.site.register(models.Cart)
admin.site.register(models.CartProduct)
admin.site.register(models.Order)
admin.site.register(models.Banner)
admin.site.register(models.Info)
admin.site.register(models.WishList)
admin.site.register(models.EnterProduct)