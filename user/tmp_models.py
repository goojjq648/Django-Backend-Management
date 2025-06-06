restaurant_app ready
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class UserUserprofile(models.Model):
    user = models.OneToOneField('AuthUser', models.DO_NOTHING)
    google_id = models.CharField(unique=True, max_length=128, blank=True, null=True)
    avatar_url = models.CharField(max_length=2000, blank=True, null=True)
    role = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_userprofile'
