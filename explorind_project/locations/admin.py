from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin
	
class PlaceOfInterestAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	

admin.site.register(Location, MPTTModelAdmin)
admin.site.register(PlaceOfInterest,PlaceOfInterestAdmin)
admin.site.register(Category)