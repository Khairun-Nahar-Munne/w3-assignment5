from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from guardian.shortcuts import assign_perm
from .validators import validate_image_urls 


class Location(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    center = PointField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    location_type = models.CharField(max_length=20)
    country_code = models.CharField(max_length=2)
    state_abbr = models.CharField(max_length=3, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    bedroom_count = models.PositiveIntegerField()
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = PointField()
    images = ArrayField(
        models.CharField(max_length=300), 
        blank=True, 
        default=list, 
        validators=[validate_image_urls]
    )
    
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    amenities = JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accommodations")
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Assign object-level permissions when creating an accommodation
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            assign_perm('view_accommodation', self.user, self)
            assign_perm('change_accommodation', self.user, self)
            assign_perm('delete_accommodation', self.user, self)



class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    language = models.CharField(max_length=2)
    description = models.TextField()
    policy = JSONField(default=dict)

    def __str__(self):
        return f"{self.property.title} - {self.language}"
