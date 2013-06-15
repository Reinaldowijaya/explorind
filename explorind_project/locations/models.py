from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import ImageField, signals
from django.dispatch import dispatcher
import os

def get_image_path(instance, filename):
    return os.path.join(str(instance.name), filename)

class Location(MPTTModel):
	name = models.CharField(max_length=50, unique=True)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	description = models.TextField()
	image = models.ImageField(upload_to=get_image_path , blank=True)	
	def __unicode__(self):
		return self.name
		
class Category(models.Model):
	category = models.CharField(max_length=50, unique=True)
	def __unicode__(self):
		return self.category
		
class PlaceOfInterest(models.Model):
	location = TreeForeignKey(Location)
	category = models.ForeignKey(Category, blank=True)
	name = models.CharField(max_length=50)
	description = models.TextField()
	def __unicode__(self):
		return self.name