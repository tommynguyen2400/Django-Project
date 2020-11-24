from django.db import models

class Manufacturer(models.Model):
    code = models.CharField(max_length=200,verbose_name='Mã',unique=True)
    name = models.CharField(max_length=200,verbose_name='Tên')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200,verbose_name='Tên',unique=True)
    code = models.CharField(max_length=200,verbose_name='Mã')
    manufacturer = models.ForeignKey(Manufacturer,verbose_name='Hãng Sản Xuất',on_delete=models.PROTECT)
    diameter = models.FloatField(verbose_name='Đường kính mặt đồng hồ (mm)') #đường kính mặt đồng hồ
    # chất liệu mặt đồng hồ
    diameter_face = models.CharField(max_length=250,verbose_name='Chất liệu mặt')
    sex = models.CharField(max_length=10,verbose_name='Giới tính',blank=True)
    # chất liệu dây đồng hồ
    material_albert = models.CharField(max_length=100,verbose_name='Chất liệu dây')

    # chất liệu vỏ
    material_case = models.CharField(max_length=100,verbose_name='Chất liệu vỏ')
    
    price = models.IntegerField(verbose_name='Giá (đ)')
    image = models.ImageField(verbose_name='Ảnh sản phẩm',upload_to='static/images')
    def priceInt(self):
        return int(self.price)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    priceUnit = models.FloatField()
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    dateOrder = models.DateTimeField()
    deliverDate = models.DateTimeField(null=True)
    status = models.IntegerField()

    class Status:
        PENDING = 0
        DELIVERED = 1
        CANCELED = 2


