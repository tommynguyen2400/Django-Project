from django.shortcuts import render,redirect,get_object_or_404
from .form_user import *
from .models import *
import math
from datetime import datetime
from django.db.models import Q
priceRanges = [
    {'min': 0, 'max': 10, 'label': 'Dưới 10 triệu'},
    {'min': 10, 'max': 15, 'label': 'Từ 10 đến 15 triệu'},
    {'min': 15, 'max': 20, 'label': 'Từ 15 đến 20 triệu'},
    {'min': 20,  'label': 'Trên 20 triệu'}    
]
def home(request):
    queryParams = request.GET
    productName = queryParams.get('product_name')
    manufacturerId = queryParams.get('manufacturer_id')
    priceRanges = queryParams.get('price_range')
    products = Product.objects.all()

    if productName:
        products = products.filter(name__contains=productName)

    if manufacturerId:
        products = products.filter(manufacturer=Manufacturer.objects.get(id=manufacturerId))

    context=  {
        'queryParams': queryParams,
        'products': products,
        'priceRanges': priceRanges,
        'manufacturers': Manufacturer.objects.all(),
    }
    return render(request,'user/base.html',context)


def products(request):
    PAGE_SIZE = 12
    page = int(request.GET.get('page') or 1)
    queryParams = request.GET
    productName = queryParams.get('product_name')
    manufacturerId = queryParams.get('manufacturer_id')
    priceRange = queryParams.get('price_range')
    sex = queryParams.get('sex_id') 
    origin = queryParams.get('origin_id')
    keyword = request.GET.get('keyword', '')
    products = Product.objects.filter(
                        Q(name__icontains=keyword) | Q(code__icontains=keyword))
    if productName:
        products = products.filter(name__contains=productName)

    if manufacturerId:
        products = products.filter(manufacturer=Manufacturer.objects.get(id=manufacturerId))

    if sex: # giới tính
        products = products.filter(sex=sex)

    if origin:
        products = products.filter(origin=origin)

    if priceRange:
        priceRange = priceRanges[int(priceRange)-1]
        minPrice = priceRange.get('min')
        maxPrice = priceRange.get('max')
        
        if minPrice:
            products = products.filter(price__gte=minPrice*1000000)
        
        if maxPrice:
            products = products.filter(price__lte=maxPrice*1000000)
    products=products.order_by('-price','name')

    start = (page-1)*PAGE_SIZE
    end = start + PAGE_SIZE
    total = len(products)
    num_page = math.ceil(total / PAGE_SIZE) #tổng số trang
    prev_page = max(page - 1,1) #trang trước
    next_page = max(page + 1,num_page) #trang tiếp
    products = products[start:end]
    context=  {
        'queryParams': queryParams,
        'products': products,
        'keyword':keyword,
        'priceRanges': priceRanges,
        'start':start,'total':total,'num_page':num_page,'prev_page':prev_page,'next_page':next_page,
        'page':page,
        'manufacturers': Manufacturer.objects.all(),
    }
    return render(request,'user/index.html',context)
def about(request):
    return render(request, 'user/about.html', {'page': 2})

def viewProduct(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'user/view_product.html', {'product': product})

def savePurchase(product, form_data):
    purchase = Purchase()
    purchase.product = product
    purchase.qty = form_data['qty']
    purchase.priceUnit = product.price
    purchase.fullname = form_data['fullname']
    purchase.phone = form_data['phone']
    purchase.address = form_data['address']
    purchase.dateOrder = datetime.now()
    purchase.status = Purchase.Status.PENDING
    purchase.save()



def purchase(request, id):
    form = PurchaseForm(initial={'qty':1})
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            savePurchase(product, form.cleaned_data)
            request.session['purchase_form'] = form.cleaned_data
            return redirect('purchase-confirm', id)
    context = {'product': product, 'form': form}
    return render(request, 'user/purchase.html', context)


def purchaseConfirm(request, id):
    product = get_object_or_404(Product, pk=id)
    form = request.session.get('purchase_form')
    return render(request, 'user/purchase_confirmation.html', {'product': product, 'form': form})


def thankYou(request):
    return render(request, 'user/thank_you.html')

