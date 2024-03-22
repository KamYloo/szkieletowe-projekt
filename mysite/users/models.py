from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_pic = models.ImageField(default="default.png")

	def __str__(self):
		return f"{self.name} {self.lastname}"
