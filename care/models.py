from django.db import models
from animals.models import Animal, Category


class Care(models.Model):
    """
   Care guide model.
    """
    name = models.CharField(max_length=30, default="")
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE,
                               related_name='care',
                               related_query_name='care')
    care_guide = models.TextField()
    cage_setup = models.TextField()
    lighting = models.TextField()
    heating = models.TextField()
    feeding_schedule = models.TextField()
    known_problems = models.TextField()
    other_information = models.CharField(max_length=100, default="")
    other_information_name = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.name
