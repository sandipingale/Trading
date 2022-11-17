from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
@login_required
def home(request):
    return render(request,'home/home.html', {})
