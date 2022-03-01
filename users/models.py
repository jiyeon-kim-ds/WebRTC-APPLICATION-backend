from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db                  import models

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name ,password):
        if not email:
            raise ValueError('email is required')
        email = self.normalize_email(email)
        user  = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        return user

class User(AbstractBaseUser):
    objects = UserManager()

    email       = models.EmailField(max_length=255, unique=True)
    first_name  = models.CharField(max_length=30)
    last_name   = models.CharField(max_length=30)
    created_at  = models.DateTimeField(auto_now_add=True)
    update_at   = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = 'email'
    
    class Meta:
        db_table='users'