from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, Http404
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
# Create your views here.
@login_required(login_url='login')
def index(request):
    all_neighborhoods = Neighborhood.get_hoods()
    
    if 'neighborhood' in request.GET and request.GET["neighborhood"]:
        neighborhoods = request.GET.get("neighborhood")
        searched_hoods = Business.get_by_hood(neighborhoods)
        all_posts = Posts.get_by_neighborhood(neighborhoods)
        message = f"{neighborhoods}"
        all_neighborhoods = Neighborhood.get_hoods() 

        context = {
            "message":message,
            "location": searched_hoods,                                 
            "all_neighborhoods":all_neighborhoods,
            "all_posts":all_posts
        }       
        
        return render(request, 'index.html', context)
    
    else:
        message = "No Neighborhood Found!" 

    context = {
        "all_neighborhoods":all_neighborhoods
    }  

    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'django_registration/registration_form', {'form': form})

@login_required(login_url='login')
def new_business(request):
    current_user = request.user
    profile = request.user.profile
    
    if request.method == 'POST':
        form = NewBusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit = False)
            business.Admin = current_user
            business.admin_profile = profile
            business.save()
            messages.success(request, 'You Have succesfully created a business')
            return redirect('index')
    else:
        form = NewBusinessForm()
        
    return render(request,'hood/new_business.html',locals())


@login_required(login_url='login')
def search_results(request):
    
    if 'Business' in request.GET and request.GET["Business"]:
        search_term = request.GET.get("Business")
        searched_Business = Business.search_by_title(search_term)
        message = f"{search_term}"

        context = {
            "message":message,
            "Business": searched_Business
        }

        return render(request, 'all-hood/search.html',context)

    else:
        message = "You haven't searched for any term"

        return render(request, 'hood/search_hood.html',{"message":message})

