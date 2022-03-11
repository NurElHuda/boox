from django.db import models


from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, EmailValidator
from django.db import DEFAULT_DB_ALIAS, models
from django.db.models.fields import DateField

from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    USER_TYPE = [
        ("Admin", "Admin"),
        ("Seller", "Seller"),
    ]

    name = models.CharField(_("Name"), blank=True, max_length=255, default="")
    email = models.EmailField(_("Email"), max_length=255, unique=True, validators=[EmailValidator,])


    is_admin = models.BooleanField(_("IsAdmin"), default=False)
    is_seller = models.BooleanField(_("IsSeller"), default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Only set as deleted if it is not already deleted.
        if not self.deleted_at:
            self.updated_at = timezone.now()
            self.deleted_at = timezone.now()
            self.is_active = False
            self.username = f"{self.username}_{self.pk}_deleted"
            self.email = f"{self.email}_{self.pk}_deleted"
            self.save()

            # if self.type != "unknown":
            #     getattr(self, self.type).delete()

    def __str__(self):
        return f"{self.pk} | {self.name}"

    @property
    def type(self):
        if self.is_admin:
            return "admin"
        elif self.is_seller:
            return "seller"
        else:
            return "unknown"


def create_user(user_validated_data):
    password = user_validated_data.pop("password", False)
    user = User.objects.create(**user_validated_data)

    if password:
        user.set_password(password)
    user.save()
    return user


def update_user(user, validated_data):
    pw = validated_data.pop("password", False)
    if pw:
        user.set_password(pw)

    for key, value in validated_data.items():
        setattr(user, key, value)

    user.save()
    return user

