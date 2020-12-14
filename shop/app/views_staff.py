from .models import *
from .form_staff import *
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

# Staff
@login_required
def listProduct(request):
    products = Product.objects.all()
    return render(request,'staff/products/list.html',{'products':products})

@login_required
def createProduct(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    return render(request,'staff/products/form.html',{'form':form})

@login_required
def updateProduct(request,id):
    p = get_object_or_404(Product,pk=id)
    form = ProductForm(instance=p)
    if request.method=='POST':
        form = ProductForm(request.POST,request.FILES,instance=p)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    return render(request,'staff/products/form.html',{'form':form})

@login_required
def deleteProduct(request, id):
    p = get_object_or_404(Product, pk=id)
    p.delete()
    return redirect('product-list')




# Manufacturer
@login_required
def listManufacturer(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'staff/manufacturer/list.html', {'manufacturers': manufacturers})

@login_required
def createManufacturer(request):
    form = ManufacturerForm()
    
    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manufacturer-list')

    return render(request, 'staff/manufacturer/form.html', {'form': form})

@login_required
def updateManufacturer(request, id):
    m = get_object_or_404(Manufacturer, pk=id)
    form = ManufacturerForm(instance=m)
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, instance=m)
        if form.is_valid():
            form.save()
            return redirect('manufacturer-list')
    return render(request, 'staff/manufacturer/form.html', {'form': form})

@login_required
def deleteManufacturer(request, id):
    m = get_object_or_404(Manufacturer, pk=id)
    m.delete()
    return redirect('manufacturer-list')  



# Order
@login_required
def listOrder(request):
    purchaseList = Purchase.objects.all()
    purchaseList = purchaseList.order_by('status', 'dateOrder')
    context = {'purchaseList': purchaseList}
    return render(request, 'staff/order/list.html', context)

@login_required
def viewOrder(request, pk):
    purchase = Purchase.objects.get(pk=pk)    #get_object_or_404
    context = {'purchase': purchase}
    return render(request, 'staff/order/detail.html', context)    

@login_required
def confirmOrder(request, pk):
    form = PurchaseConfirmForm()
    if request.method == 'POST':
        form = PurchaseConfirmForm(request.POST)
        if form.is_valid():
            purchase = Purchase.objects.get(pk=pk)
            purchase.status = Purchase.Status.DELIVERED
            purchase.deliverDate = form.cleaned_data['deliverDate']
            purchase.save()
            return redirect('/list_order')
    context = {'form': form}
    return render(request, 'staff/order/confirm.html', context)

def cancelOrder(request, pk):
    if request.method == 'POST':
        purchase = Purchase.objects.get(pk=pk)
        purchase.status = Purchase.Status.CANCELED
        purchase.save()
        return redirect('/list_order')
    return render(request, 'staff/order/cancel.html')   
