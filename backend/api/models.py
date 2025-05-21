from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class FirebaseUserManager(BaseUserManager):
    def create_user(self, uid, email=None):
        if not uid:
            raise ValueError("Users must have a Firebase UID")
        user = self.model(uid=uid, email=email)
        user.save(using=self._db)
        return user

class FirebaseUser(AbstractBaseUser):
    uid = models.CharField(max_length=128, unique=True)  # From Firebase
    email = models.EmailField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = FirebaseUserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or self.uid

    @property
    def is_staff(self):
        return self.is_admin
