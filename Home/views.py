from django.shortcuts import render
from ESOKO.models import Product

# Create your views here.
def HomeView(request):
    product=Product.objects.all().order_by('-created_at')[:6]
    featured_product = Product.objects.filter(valid=True).order_by('-created_at').first()
    context={'products':product,'featured_product':featured_product}
    return render(request,'homepage.html',context)