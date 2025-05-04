from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .managers import UserManager

class User(AbstractBaseUser):
	username = models.CharField(max_length=100, unique=True)
	email = models.EmailField(default="")
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = "username"

	objects = UserManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_superuser

	def has_module_perms(self, app_label):
		return self.is_superuser