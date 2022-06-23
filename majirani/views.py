from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from .email import send_welcome_email
from django.contrib.auth import login, authenticate
# Create your views here.
@login_required(login_url='login')
def index(request):
    all_hoods = Neighborhood.objects.all()
    all_hoods = all_hoods[::-1]

    return render(request, 'index.html', locals())

def register(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        procForm=ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid() and procForm.is_valid():
            username=form.cleaned_data.get('username')
            user=form.save()
            profile=procForm.save(commit=False)
            profile.user=user
            profile.save() 

            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)
        return redirect('login')
    else:
        form= SignupForm()
        prof=ProfileUpdateForm()
    context={
        'form':form,
        'profForm': prof
    }
    return render(request, 'registration/registration.html', context)

@login_required(login_url='login')
def new_business(request):
	'''
	View function that enables users to add businesses
	'''
	if request.method == 'POST':
		form = NewBusinessForm(request.POST)
		if form.is_valid():
			business_form = form.save(commit = False)
			business_form.user = request.user
			business_form.save()
			messages.success(request, 'You Have succesfully created a business')
			return redirect('my_hood')

	else:
		form = NewBusinessForm()
		return render(request,'hood/new_business.html',locals())


@login_required(login_url='login')
def search_results(request):
    if request.method == 'GET':
        name = request.GET.get('title')
        results = Business.objects.filter(name__icontains=name).all()
        message = f'name'
        context = {
      'results': results,
      'message': message
     }
        return render(request, 'hood/search_hood.html', context)
    else:
        message = 'Search a business name for results'

    return render(request, 'hood/search_hood.html',{"message":message})

@login_required(login_url='login') 
def create_hood(request):
  if request.method == 'POST':
    form = NewNeighborhoodForm(request.POST, request.FILES)
    if form.is_valid():
      hood = form.save(commit=False)
      hood.admin = request.user.profile
      hood.save()
      return redirect('index')
  else:
    form = NewNeighborhoodForm()
  return render(request, 'hood/create_hood.html', {'form': form})

@login_required(login_url='login')
def new_post(request):
    
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
        return redirect('all_posts')
    else:
        form = NewPostForm()
    return render(request, 'hood/new_post.html', {"form":form})

@login_required(login_url='login')
def edit_profile(request, profile_id):
    user = request.user
    # user = user.objects.get(username=username)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        prof_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.id)
    else:
        user_form = UserUpdateForm(instance=request.user)
        prof_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'profile/update_profile.html', context )

def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, 'userprofile.html', params)

@login_required(login_url='login')
# def my_hood(request, hood_id):
#     hood = Neighborhood.objects.get(id=hood_id)
#     business = Business.objects.filter(neighbourhood=hood)
#     posts = Posts.objects.filter(hood=hood)
#     posts = posts[::-1]
#     if request.method == 'POST':
#         form = NewBusinessForm(request.POST)
#         if form.is_valid():
#             business_form = form.save(commit=False)
#             business_form.neighbourhood = hood 
#             business_form.user = request.user.profile
#             business_form.save()
#             return redirect('my_hood', hood_id)
#     else:
#         form = NewBusinessForm()
#     context = {
#     'hood': hood,
#     'business': business,
#     'form': form,
#     'posts': posts,
#   }
#     return render(request, 'hood/my_hood.html', context)

def all_hoods(request):
    all_hoods = Neighborhood.objects.all()
    all_hoods = all_hoods[::-1]
    return render(request, 'index.html', locals())

def all_posts(request):
    all_posts = Posts.objects.all()
    all_posts = all_posts[::-1]
    return render(request, 'hood/hood_posts.html', locals())

def all_works(request):
    all_works = Business.objects.all()
    all_works = all_works[::-1]
    return render(request, 'hood/all_works.html', locals())