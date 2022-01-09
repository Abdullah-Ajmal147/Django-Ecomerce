from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    products = Product.objects.all().filter(is_avaiable=True)
    return render(request, 'home.html', {'products': products})