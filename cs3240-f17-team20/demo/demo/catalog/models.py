from django.db import models
from django.urls import reverse

# Create your models here.
class Person(models.Model):
    Name = models.CharField(max_length=20, help_text="Enter a name")

    Age = models.IntegerField(help_text="Enter an age")

    class Meta:
        ordering = ["Name"]

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('model-detail-view', args=[str(self.id)])


class Friend(models.Model):
    Name = models.CharField(max_length=20, help_text="Enter a name")

    Age = models.IntegerField(help_text="Enter an age")

    class Meta:
        ordering = ["Name"]

    def __str__(self):
        return "The friend" + self.Name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('model-detail-view', args=[str(self.id)])
