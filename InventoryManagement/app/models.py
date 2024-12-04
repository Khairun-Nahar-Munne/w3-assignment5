from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from guardian.shortcuts import assign_perm
from langdetect import detect 
from django.core.exceptions import ValidationError
from .validators import validate_images_field 

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

def validate_amenities(value):
    for item in value:
        if len(item) > 100:
            raise ValidationError(f"Amenity '{item}' exceeds 100 characters.")


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
        models.CharField(max_length=300),  # Each URL can have a maximum of 300 characters
        blank=True,                        # Allows the field to be optional
        default=list,                       # Sets the default value to an empty list
        validators=[validate_images_field] 
    )
    
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    amenities = models.JSONField(default=list, validators=[validate_amenities])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accommodations")
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.title
    def clean(self):
        # Check that country_code matches the country_code of the Location
        if self.location and self.country_code != self.location.country_code:
            raise ValidationError(
                f"The country code ({self.country_code}) must match the country code of the selected location ({self.location.country_code})."
            )
          # Get the images field (comma-separated string)
        images_input = self.images
        
        # If the input is a string, split it into a list
        if isinstance(images_input, str):
            # Split the string by commas and strip extra spaces
            self.images = [url.strip() for url in images_input.split(',')]
        
        # Now validate the images
        validate_images_field(self.images)
       
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

    def clean(self):
        # Detect language of description
        detected_description_language = detect(self.description)
        if detected_description_language.startswith('zh'):
            detected_description_language = 'zh'

        if detected_description_language != self.language:
            raise ValidationError(f"The description is not in the selected language ({self.language}). Detected language: {detected_description_language}")
            
        
        # Detect language for each policy value
        for policy_key, policy_value in self.policy.items():
            detected_policy_language = detect(policy_value)
        if detected_policy_language.startswith('zh'):
            detected_policy_language = 'zh'

        if detected_policy_language != self.language:
            raise ValidationError(f"The policy '{policy_key}' is not in the selected language ({self.language}). Detected language: {detected_policy_language}")


    def __str__(self):
        return f"{self.property.title} - {self.language}"

