from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_pic = models.ImageField(default="default.png", upload_to="profile_pics")

	def __str__(self):
		return f"{self.user.first_name} {self.user.last_name}"

	def save(self):
		super().save()

		img = Image.open(self.profile_pic.path)

		if img.height > 256 or img.width > 256:
			output_size = (256, 256)
			img.thumbnail(output_size)
			img.save(self.profile_pic.path)