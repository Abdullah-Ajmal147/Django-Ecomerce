from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from category.models import Category
from django.db.models import Q

from cart.views import _cart_id
from cart.models import CartItem
from  django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def search(request):
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            product = Product.objects.order_by('-created_date').filter(Q(description__icontains=keywords) | Q(product_name__icontains=keywords))

    content = {
        'products': product,
    }
    return render(request, 'store.html', content)

def product_details(request,category_slug, product_slug):
     try: 
        single_product = Product.objects.get(category__slug=category_slug, slug= product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

     except Exception as e:
        raise e  
     context={
      'single_product': single_product,  
      'in_cart': in_cart
    }
         
     return render(request, 'product_details.html', context)
   # return HttpResponse("test")
def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)  
        products = Product.objects.filter(category= categories, is_avaiable=True).order_by('id')
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)

        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_avaiable=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)

        product_count = products.count()
    # products = Product.objects.all().filter(is_avaiable=True)
    # product_count = products.count()
    context= {
        'products': page_product,
        'count': product_count,
    }
    #return HttpResponse("hello there")
    return render(request,'store.html', context)