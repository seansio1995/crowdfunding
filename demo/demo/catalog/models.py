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

class Report(models.Model):
    company = models.CharField(max_length=30, help_text="Company name")

    phone = models.CharField(max_length=20, help_text="Company phone number")

    location = models.CharField(max_length=20, help_text="Company location")

    country = models.CharField(max_length=30, help_text="Company country")

    sector = models.CharField(max_length=30, help_text="Company sector")

    industry = models.CharField(max_length=30, help_text="Company industry")

    class Meta:
        ordering = ["company"]

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])





