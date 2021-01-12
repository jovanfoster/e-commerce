from django.db import models
from ecommerce_website import settings


class Product(models.Model):
    name        =   models.CharField(max_length=120)
    price       =   models.DecimalField(max_digits=10, decimal_places=2)
    description =   models.TextField(null=True)
    featured    =   models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        return self.images.first().image.url

    @property
    def has_second_image(self):
        images = self.images.all()
        if len(images) > 1:
            return True
        else:
            return False

    @property
    def second_image(self):
        images = self.images.all()
        return images[1].image

    @property
    def serialized_price(self):
        return str(self.price)
 

class ProductImage(models.Model):
    name = models.CharField(max_length=120)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images') 
    image = models.ImageField(upload_to=settings.STATIC_URL.join('imgs/'))


class Review(models.Model):
    user        =   models.ForeignKey('users.MyUser', on_delete=models.CASCADE)
    product     =   models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    rating      =   models.IntegerField()
    summary     =   models.TextField()
    date_posted =   models.DateField(auto_now=True)


class Category(models.Model):
    title       =   models.CharField(max_length=120)
    # a category can have many products and a product can have many categories
    products    =   models.ManyToManyField(Product, related_name='category') 

    def __str__(self):
        return self.title    
