from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from random import sample
import string

class Banner(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    images = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='category-img')
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    @property
    def subcategorieslist(self):
        subcategory = SubCategory.objects.filter(
            category=self.id
        ).order_by('id')
        return subcategory
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='subcategory-img')
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    @property
    def productlist(self):
        product = Product.objects.filter(
            subcategory=self.id
        ).order_by('id')
        return product

    def __str__(self):
        return self.name


class Product(models.Model):
    name:str = models.CharField(max_length=255)
    quantity:int = models.PositiveIntegerField(default=1)
    price:float = models.DecimalField(max_digits=8, decimal_places=2)
    subcategory:SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description:str = models.TextField()
    img = models.ImageField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='product-img')

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    shopping_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.author.username
    

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name
    
    @property
    def total(self):
        return self.product.price * self.quantity


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=255)
    status = models.SmallIntegerField(
        choices=(
            (1, 'готовится'),
            (2, 'в пути'),
            (3, 'в зоне подачи'),
            (4, 'забрали'),
            (5, 'отказано'),
        )
    )

    def __str__(self):
        return self.full_name
    

class Info(models.Model):
    phone = models.CharField(max_length=233)
    region = models.TextField()
    text = models.TextField()
    email = models.URLField(max_length=233, blank=True, null=True)
    facebook = models.URLField(max_length=233, blank=True, null=True)
    twitter = models.URLField(max_length=233, blank=True, null=True)
    linking = models.URLField(max_length=233, blank=True, null=True)


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username}, {self.product.name}"


class EnterProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    enter_quantity = models.IntegerField(default=1)
    old_quantity = models.IntegerField(blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    time = models.TimeField(auto_now_add=True, blank=True, null=True)
    info = models.TextField()

    def __str__(self) -> str:
        return self.product.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.old_quantity = self.product.quantity
        else:
            previous_entry = EnterProduct.objects.get(id=self.id)
            self.old_quantity = previous_entry.enter_quantity
        self.product.quantity += self.enter_quantity - self.old_quantity
        super(EnterProduct, self).save(*args, **kwargs)