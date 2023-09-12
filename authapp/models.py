from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    

    def create_superuser(self,email,password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True 
        user.is_staff =True 
        user.is_active = True 
        user.save(using=self._db)
        return user 


class User(AbstractBaseUser,PermissionsMixin):
    '''
    '''
    first_name = models.CharField(max_length=50,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(null=False,blank=False,unique=True,error_messages={
        "unique" : "An account with this email exist"
    })
    is_superuser = models.BooleanField(default=False)
    
    is_staff = models.BooleanField(default=False)
    
    full_name = models.CharField(max_length=100,null=True,blank=True)
    
    is_updated = models.BooleanField(default=False)
    
    updated_at = models.DateTimeField(null=True,blank=True)

    created_at = models.DateTimeField(null=False,blank=False)
    
    objects = UserManager()

    USERNAME_FIELD = "email"

    def save(self,*args,**kwargs):
        if self.last_name:
            self.full_name = self.first_name.title() + " " + self.last_name.title()
        else:
            self.full_name = self.first_name.title()
        
        # no  matter in which format email is passed from client, inside DB we will maintain a uniform (lower) case only,

        self.email = self.email.lower()

        super(User,self).save(*args,**kwargs)
    
    class Meta:
        db_table = "UserTable"
    