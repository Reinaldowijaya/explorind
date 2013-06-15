from django.http import  HttpResponse
from django.shortcuts import render,render_to_response, get_object_or_404,redirect
from .models import *
from reviews.models import Review , Review_Comment
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import AuthenticateForm, UserCreateForm
from reviews.forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

def index(request, auth_form=None, user_form=None):

	if request.user.is_authenticated():
		review_form = ReviewForm()
		user = request.user
		review_self = Review.objects.filter(user=user.id)
		review_friends = Review.objects.filter(user__userprofile__in=user.profile.follows.all)
		reviews = review_self | review_friends
	
		return render (request,
						'buddies.html',
						{'review_form': review_form, 'user': user,
						 'reviews':reviews,
						 'next_url':'/'})
						 
	else:	
		auth_form = auth_form or AuthenticateForm()
		user_form = user_form or UserCreateForm()
 
        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })
					  
							
def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')
def logout_view(request):
    logout(request)
    return redirect('/')
	
def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')

@login_required
def submit(request):
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if review_form.is_valid():
			review = review_form.save(commit=False)
			review.user = request.user
			review.save()
			return redirect(next_url)
        else:
            return public(request, review_form)
    return redirect('/')

@login_required
def public(request, review_form=None):
    review_form = review_form or ReviewForm()
    reviews = Review.objects.reverse()[:10]
    return render(request,
                  'public.html',
                  {'review_form': review_form, 'next_url': '/review',
                   'reviews': reviews, 'username': request.user.username})
def get_latest(user):
    try:
        return user.review_set.order_by('-id')[0]
    except IndexError:
        return ""
@login_required
def users(request, username="", review_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        reviews = Review.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile or buddies' profile
            return render(request, 'user.html', {'user': user, 'reviews': reviews, })
        return render(request, 'user.html', {'user': user, 'reviews': reviews, 'follow': True, })
    users = User.objects.all().annotate(review_count=Count('review'))
    reviews = map(get_latest, users)
    obj = zip(users, reviews)
    review_form = review_form or ReviewForm()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                   'review_form': review_form,
                   'username': request.user.username, })
@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')
		
