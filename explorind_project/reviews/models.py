from django.db import models
from django.contrib.auth.models import User
from locations.models import PlaceOfInterest

def get_image_path(instance, filename):
    return os.path.join('user',str(user),'review', filename)

class Review(models.Model):
	placeofinterest = models.ForeignKey(PlaceOfInterest)
	user = models.ForeignKey(User)
	text = models.CharField(max_length = 225, blank=True)
	created = models.DateTimeField(auto_now=True, blank=True)
	rating = models.BooleanField()
	image = models.ImageField(upload_to=get_image_path, blank=True)
	def __unicode__(self):
		return self.name
		
class Review_Comment(models.Model):
	review = models.ForeignKey(Review)
	text = models.CharField(max_length = 225)
	user = models.ForeignKey(User)
