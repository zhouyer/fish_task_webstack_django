from django.shortcuts import render
from .models import FirstLevelMenuItem


# Create your views here.

def index(request):
    first_level_menu = FirstLevelMenuItem.objects.all().order_by('sort')
    return render(request, 'webstack/index.html', context={'first_level_menu': first_level_menu})
