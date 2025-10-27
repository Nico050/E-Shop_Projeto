from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    p_pic = models.ImageField(upload_to='profile_pics/', default='default.png', verbose_name="Foto de perfil")

    def __str__(self):
        return f"Perfil de {self.user.username}"


# Create your models here.
