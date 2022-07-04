from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Category class.
    """
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Animal(models.Model):
    """
    Animal model.
    """
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    animal_id = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30)
    latin_name = models.CharField(max_length=30)
    country = models.CharField(max_length=30, default="")
    climate = models.CharField(max_length=30)
    temperament = models.CharField(max_length=50, default="")
    food = models.CharField(max_length=50, default="")
    min_tank_size = models.CharField(max_length=30)
    max_length = models.CharField(max_length=30, default="")
    lifespan = models.CharField(max_length=30, default="")
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    temperature = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.name


class Rating(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE,
                               related_name='rating',
                               related_query_name='rating',
                               null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True,
                             )
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    rating_out_of_five = models.IntegerField(default=0)

    def __str__(self):
        return self.title
