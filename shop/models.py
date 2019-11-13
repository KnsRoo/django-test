from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models

class Categories(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=400)

class Goods(models.Model):
	name = models.CharField(max_length=50)
	image = models.ImageField(blank=True, upload_to = "gallery/")
	category = models.ForeignKey(Categories, on_delete = models.CASCADE)
	count = models.IntegerField()
	price = models.FloatField()
	description = models.CharField(max_length=400)
