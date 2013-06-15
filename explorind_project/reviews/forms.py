from django import forms
from django.contrib.auth.models import User
from .models import Review

class ReviewForm(forms.ModelForm):
    
    def is_valid(self):
        form = super(ReviewForm, self).is_valid()
        for f in self.errors.iterkeys():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error reviewText'})
        return form
 
    class Meta:
        model = Review
        fields = ['placeofinterest', 'text', 'rating','image']