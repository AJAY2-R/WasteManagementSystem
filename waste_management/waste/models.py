from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#creating tables in django
class user_Registration(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(null=True,max_length=100) 
    address=models.CharField(null=True,max_length=100) 
    pincode=models.CharField(null=True,max_length=20)
    password=models.CharField(null=True,max_length=100)
    name=models.CharField(null=True,max_length=100)
    email=models.CharField(null=True,max_length=100)
    point=models.IntegerField(default=0)

class userType(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    type=models.CharField(null=True,max_length=100)

class collector_Registration(models.Model):
    mobile=models.CharField(null=True,max_length=100)
    address=models.CharField(null=True,max_length=100)
    password=models.CharField(null=True,max_length=100)
    name=models.CharField(null=True,max_length=100)
    email=models.CharField(null=True,max_length=100)
    collector_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
class products(models.Model):
    name=models.CharField(max_length=100,null=True)
    rate=models.IntegerField(null=True)
    point=models.IntegerField(null=True)
    desc=models.CharField(max_length=200,null=True)
    image=models.ImageField(null=True,upload_to='images')
    status=models.IntegerField(null=False)
    
class stock_his(models.Model):
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    stock=models.IntegerField(null=True)

class category(models.Model):
    name=models.CharField(max_length=100)
    point=models.IntegerField(null=True)

class waste_pickup(models.Model):
    userid=models.ForeignKey(user_Registration,on_delete=models.CASCADE,null=True)
    collector=models.ForeignKey(collector_Registration,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,default='requested')
    rdate=models.DateField(default=timezone.now)
    pdate=models.DateField(null=True)


class CollectionHistory(models.Model):
    pid = models.ForeignKey(waste_pickup, on_delete=models.CASCADE)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    weight = models.FloatField(null=True)
    point = models.IntegerField(null=True)

class Purchase(models.Model):
    user=models.ForeignKey(user_Registration,on_delete=models.CASCADE,null=True)
    date=models.DateField(default=timezone.now)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    mobile=models.CharField(null=True,max_length=100)
    address=models.CharField(null=True,max_length=100)
    pincode=models.CharField(null=True,max_length=20)
    quantity=models.CharField(null=True,max_length=1,default=1)
    REDEEM='R'
    PURCHASE='P'
    CHOICE=[(REDEEM,'Redeem'),(PURCHASE,'Purchase')]
    type=models.CharField(max_length=2,choices=CHOICE)
    total=models.IntegerField(null=True)
    status=models.CharField(max_length=20,null=True,default='Ordered')
    
class OrderUpdates(models.Model):
    order=models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True)
    date=date=models.DateField(default=timezone.now)
    status=models.CharField(max_length=20,null=True,default='Ordered')
    update=models.CharField(null=True,max_length=100)

class Comaplaints(models.Model):
    user=models.ForeignKey(user_Registration,on_delete=models.CASCADE,null=True)
    subject=models.CharField(null=True,max_length=100)
    complaint=models.CharField(null=True,max_length=200)
    rdate=models.DateField(default=timezone.now)
    sdate=models.DateField(null=True)
    status=models.CharField(max_length=20,null=True,default='Pending')

class locations(models.Model):
    pincode=models.CharField(max_length=10,null=True)