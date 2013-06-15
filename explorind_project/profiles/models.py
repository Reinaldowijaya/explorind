from django.db import models
from django.contrib.auth.models import User
from locations.models import Category
# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('user',str(instance.name), filename)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	follows = models.ManyToManyField( 'self', related_name = 'followed_by', symmetrical = False)
	category = models.ForeignKey(Category,blank = True, null = True)
	avatar = models.ImageField(upload_to=get_image_path,blank=True)
	def __unicode__(self):
		return self.name
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])