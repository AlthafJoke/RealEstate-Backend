from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("users must have email address")
        
        email = self.normalize_email(email)
        email = email.lower()
        
        user = self.model(
            email=email,
            name=name
            
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    
    def create_employer(self, email, name, password=None):
        user = user.create_user(email, name, password)
        
        user.is_employer = True
        
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        
        user.is_superuser =True
        user.is_staff = True
        
        user.save(using=self._db)
        
        return user
        
        







class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email
    
    
    
