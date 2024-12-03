# app/validators.py

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import re

# Custom validator to check if the URL points to an image
def validate_image_url(url):
    # Use the URLValidator to check if the URL is well-formed
    url_validator = URLValidator()
    try:
        url_validator(url)
    except ValidationError:
        raise ValidationError(f"{url} is not a valid URL.")
    
    # Regex to check if the URL ends with an image file extension (e.g., .jpg, .png, .gif)
    if not re.match(r'http(s?):\/\/.*\.(jpg|jpeg|png|gif|bmp|tiff|webp)$', url):
        raise ValidationError(f"{url} is not a valid image URL.")

# Custom validator to validate multiple image URLs from a single input
def validate_images_field(value):
    if not value:
        return
    
    # Check if value is a list (as it should be for an ArrayField)
    if isinstance(value, list):
        for url in value:
            validate_image_url(url)  # Validate each URL individually
    else:
        # If the value is not a list, raise a validation error
        raise ValidationError("The images field should be a list of URLs.")
