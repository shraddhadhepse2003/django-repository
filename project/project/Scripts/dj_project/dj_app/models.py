from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    c_name=models.CharField(max_length=30)
    
    class Meta:
        db_table:'category'

    def __str__(self):
        return self.c_name

class Product(models.Model):
    img=models.ImageField(upload_to='image',default='')
    p_name=models.CharField(max_length=50)
    p_price=models.IntegerField()
    p_description=models.TextField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    class Meta:
        db_table:'product'

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        db_table='cart'



    

    
