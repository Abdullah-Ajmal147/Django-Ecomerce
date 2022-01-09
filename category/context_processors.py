from .models import Category

def menu_link(requst):
    links= Category.objects.all()
    return dict(links=links)