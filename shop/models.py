from django.db import models

# Create your models here.

class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    product_desc = models.CharField(max_length=500)
    product_date = models.DateField()
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=20, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    add1 = models.CharField(max_length=100)
    add2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

class OrderUpdates(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.update_desc[0:8]+"..."

