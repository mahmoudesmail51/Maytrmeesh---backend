from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager , PermissionsMixin




from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """ Manager for users"""
    def create_user(self,email,password):
        """ creates a new user"""

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using = self._db)

        return user
    
    def create_superuser(self,email,password):
        """ Creates a super user"""
        user = self.create_user(email,password)

        user.is_staff= True
        user.is_superuser = True
        user.save(using= self._db)

        return user


class User(AbstractBaseUser,PermissionsMixin):
    """ Database model for users"""
    email = models.EmailField(max_length=255, unique=True)
    is_customer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """ returns string representation of object"""
        return self.email


class CustomerManager(models.Manager):
    """ Manager for Customer"""
    def create_customer(self, user, first_name, last_name, date_of_birth, phone_number):
        """ Creates new customer"""
        customer = self.model(user = user, first_name=first_name, last_name=last_name,
                            date_of_birth=date_of_birth, phone_number= phone_number)
        customer.save(using=self._db)
        return customer

class Customer(models.Model):
    """ Database model for customers"""
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=11)

    objects = CustomerManager()

    def __str__(self):
        return self.first_name +" "+ self.last_name

#Automatically generates auth-token for users saved in the system
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class FoodVenueManager(models.Manager):
    """ return objects with location x"""
    def get_venues(location):
        return FoodVenue.objects.filter(location = "x")

class FoodVenue(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField()
    bank_account_number = models.CharField(max_length=255)
    objects = FoodVenueManager()
