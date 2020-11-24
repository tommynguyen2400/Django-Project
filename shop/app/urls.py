from django.urls import path,include
from . import views,views_staff,views_user
urlpatterns=[
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/signup',views.signup),

    ############# Staff ##########
    path('staff',views_staff.listProduct,name='product-list'),
    path('staff/product_create',views_staff.createProduct,name='product-create'),
    path('staff/product_update/<int:id>',views_staff.updateProduct,name='product-update'),
    path('staff/product_delete/<int:id>',views_staff.deleteProduct,name='product-delete'),


    # Manage manufactures
    path('staff/manufacturer_list', views_staff.listManufacturer, name='manufacturer-list'),  
    path('staff/manufacturer_create', views_staff.createManufacturer, name='manufacturer-create'),  
    path('staff/manufacturer_update/<int:id>', views_staff.updateManufacturer, name='manufacturer-update'),  
    path('staff/manufacturer_delete/<int:id>', views_staff.deleteManufacturer, name='manufacturer-delete'),

    # order
    path('list_order',views_staff.listOrder),
    path('view_order/<pk>',views_staff.viewOrder),
    path('confirm_order/<pk>',views_staff.confirmOrder),
    path('cancel_order/<pk>',views_staff.cancelOrder),


    #user
    path('', views_user.home, name='home'),
    path('products', views_user.products, name='products'),
    path('about', views_user.about, name='about'),
    path('product_detail/<int:id>', views_user.viewProduct, name='view-product'),
    path('purchase/<int:id>', views_user.purchase, name='purchase'),
    path('purchase_confirm/<int:id>', views_user.purchaseConfirm, name='purchase-confirm'),
    path('thank_you', views_user.thankYou, name='thank-you'), 
]
