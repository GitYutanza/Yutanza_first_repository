from django.shortcuts import render
from djandoapp_2.settings import *
from .scraype import scrape

def DoScrape(request):
    scrape()
    return render(request,  os.path.join(BASE_DIR, 'second_app/templates/success.html'))

# Create your views here.
