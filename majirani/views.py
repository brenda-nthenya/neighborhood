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
    pass

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


