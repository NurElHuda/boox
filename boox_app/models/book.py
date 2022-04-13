from django.db import models


from django.db import models
from django.urls import reverse

from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class Book(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)


    seller = models.ForeignKey(
        "boox_app.User",
        verbose_name=_("Seller"),
        related_name="books",
        on_delete=models.CASCADE,
    )

    title = models.CharField(_("Title"), blank=True, max_length=255, default="")
    cover = models.CharField(_("Cover"), blank=True, max_length=512, default="")
    author_name = models.CharField(_("Author's name"), blank=True, max_length=255, default="")
    wilaya = models.CharField(_("Wilaya"), blank=True, max_length=255, default="")
    price = models.IntegerField(_("Price"), default=0)
    goodreads = models.CharField(_("Goodread"), max_length=255, default=None, blank=True, null=True)
    messenger = models.CharField(_("Messenger"), max_length=255, default=None, blank=True, null=True)
    whatsup = models.CharField(_("Whatsup"), max_length=255, default=None, blank=True, null=True)


    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.pk} | {self.title}"

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def update(self, validated_data):
        fields = []
        for key, value in validated_data.items():
            setattr(self, key, value)
            fields.append("key")

        self.save(update_fields=fields)

    def delete(self, *args, **kwargs):
        # Only set as deleted if it is not already deleted.
        if not self.deleted_at:
            self.updated_at = timezone.now()
            self.deleted_at = timezone.now()
            self.save()

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})


