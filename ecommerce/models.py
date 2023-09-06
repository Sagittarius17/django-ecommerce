from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, phn_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phn_number=phn_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Use the custom user model
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    phn_number = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=255, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'number']
    
    def __str__(self):
        return self.username

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)
    
#     def __str__(self):
#         return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    desc = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
         if i.product.digital == False:
            shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    # @property
    # def get_total(self):
    #     total = self.product.price * self.quantity
    #     return total
    
    @property
    def get_total(self):
        if self.product:
            total = self.product.price * self.quantity
            return total
        return 0
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.customer} - {self.address}'
