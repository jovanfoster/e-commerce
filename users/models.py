from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('User must have a valid email')
        if not password:
            raise ValueError('User must have a valid password')
        if not first_name:
            raise ValueError('User must have a valid first name')
        if not last_name:
            raise ValueError('User must have a valid last name')

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = False
        user.is_staff = False
        user.set_password(password) # hashes password

        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('User must have a valid email')
        if not password:
            raise ValueError('User must have a valid password')
        if not first_name:
            raise ValueError('User must have a valid first name')
        if not last_name:
            raise ValueError('User must have a valid last name')

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = True
        user.is_staff = True
        user.set_password(password) # hashes password

        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    # sets the email as the authentication field for logging in users
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager() # use a custom user manager
 
    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    def __str__(self):
        return self.email


#   store all the items for a specific order
#   one order item relates to one product on an order
class OrderItem(models.Model):
    order       =   models.ForeignKey('Order', on_delete=models.CASCADE, related_name='item')
    product     =   models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity    =   models.IntegerField(default=0)


#   store info for a specific customer's order
class Order(models.Model):
    user        =   models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='order')
    completed   =   models.BooleanField(default=False)

    def __str__(self):
        return "%s's order" % self.user.email

 