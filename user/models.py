from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserUserprofile(models.Model):
    ROLE_CHOICES = [
        ('user', '一般使用者'),
        ('admin', '後台管理員'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="useruserprofile")
    google_id = models.CharField(unique=True, max_length=128, blank=True, null=True)
    avatar_url = models.CharField(max_length=2000, blank=True, null=True)
    role = models.CharField(max_length=6, blank=True, null=True, choices=ROLE_CHOICES, default='user')

    class Meta:
        managed = False
        db_table = 'user_userprofile'