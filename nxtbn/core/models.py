import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from django_extensions.db.fields import AutoSlugField
from nxtbn.users.admin import User


class AbstractUUIDModel(models.Model):
    alias = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


    
class AbstractBaseUUIDModel(AbstractUUIDModel):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class NameDescriptionAbstract(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
class PublishableModel(AbstractBaseModel):
    published_date = models.DateTimeField(blank=True, null=True)
    is_live = models.BooleanField(default=False)

    def make_live(self):
        if not self.published_date:
            self.published_date = timezone.now()
        self.is_live = True
        self.save()

    def make_inactive(self):
        self.is_live = False
        self.published_date = None
        self.save()

    def clean(self):

        if self.is_live and not self.published_date:
            raise ValidationError("Published content must have a publication date.")

    class Meta:
        abstract = True



class AbstractSEOModel(models.Model):
    meta_title = models.CharField(
        max_length=800, blank=True, null=True, help_text="Title for search engine optimization."
    )
    meta_description = models.CharField(
        max_length=350, blank=True, null=True, help_text="Description for search engines."
    )
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        abstract = True
        verbose_name = "SEO Information"
        verbose_name_plural = "SEO Information"

class AbstractAddressModels(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.street_address}, {self.city}, {self.country}"
