from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Product_Category
from .add_product_form import AddProductForm
# Create your views here.
class ESOKOView(View):
    def get(self,request,id=None):
        if id is not None:
            product=Product.objects.get(id=id)
            product_categories = Product_Category.objects.all()
            recommended_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
            context={'product':product_categories,"product":product,'recommended_products':recommended_products}
            return render(request,'singleProduct.html',context)
        products=Product.objects.all()[:15]
        product_categories = Product_Category.objects.all()
        context={'product_categories':product_categories,"form":AddProductForm,"products":products}
        return render(request,'ESOKO.html',context)
    def post(self,request):
        form=AddProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            product_categories = Product_Category.objects.all()
            context={'product_categories':product_categories}
            return redirect('/esoko')
        else:
            print(form.errors)
            product_categories = Product_Category.objects.all()
            context={'product_categories':product_categories,"form":AddProductForm}
            return render(request,'ESOKO.html',context)
        
def category_products(request,id=None):
    if id is not None:
        category=Product_Category.objects.get(id=id)
        products=Product.objects.filter(category=category)
        product_categories = Product_Category.objects.all()
        context={'product_categories':product_categories,"category_products":products}
        return render(request,'ESOKO.html',context)
    