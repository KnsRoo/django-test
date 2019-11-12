from django.db import models

# Create your models here.

class Categories(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=400)

class Goods(models.Model):
	name = models.CharField(max_length=50)
	image = models.BinaryField(blank=True)
	category = models.ForeignKey(Categories, on_delete = models.CASCADE)
	count = models.IntegerField()
	price = models.FloatField()
	description = models.CharField(max_length=400)
