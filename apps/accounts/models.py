from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from apps.services.emails import send_account_approved_email
from django.core.mail import send_mail

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)

class EmailBasedUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Required fields for Django admin/permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    # Link the Custom Manager
    objects = CustomUserManager()

    # Define what field is used for logging in
    USERNAME_FIELD = 'email'
    
    # Fields required when using `python manage.py createsuperuser`
    REQUIRED_FIELDS = ['full_name'] 

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_instance =   EmailBasedUser.objects.get(pk=self.pk)
            if old_instance.is_active != self.is_active: # and self.is_active == is_active:
                send_account_approved_email(self)
        return super().save(*args, **kwargs)

    def send_status_email(self, email):
        send_mail(
                subject="Registration approved",
                message=f"The task has been marked as completed.",
                from_email="agesxpat@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )