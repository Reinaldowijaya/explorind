# Create your views here.
from django.shortcuts import render,render_to_response, get_object_or_404
from locations.models import Location, PlaceOfInterest

def view_location(request, name):
		
		location = get_object_or_404(Location,name=name)
		return render(request, 'Location.html', {'location':location})

		
def location(request, locationname="",placeofinterest=""):	
    if locationname:
        #Show a location
        try:
            locationname = Location.objects.get(name=locationname)	
        except Location.DoesNotExist:
            raise Http404
        # reviews = Review.objects.filter(user=user.id)
		
	if placeofinterest:
		#Show Place of interest
		try:
			placeofinterest = PlaceOfInterest.objects.get(location=locationname,name=placeofinterest)
		except PlaceOfInterest.DoesNotExist:
			return render(request, 'Location.html', {'location':locationname})	
			
		return render(request, 'PlaceOfInterest.html', {'placeofinterest':placeofinterest})	
	else:
		return render(request, 'Location.html', {'location':locationname})	

def view_placeofinterest(request,name):
	return render_to_response('view_placeofinterest.html', {
		'placeofinterest': get_object_or_404(PlaceOfInterest)
		#'reviews' : Review.objects.filter(placeofinterest=placeofinterest)[:5]
		
		})