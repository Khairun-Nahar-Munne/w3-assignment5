from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from urllib.parse import urlparse

def validate_image_urls(value):
    """
    Validates a single image URL or a list/array of image URLs.
    Automatically wraps single string input into a list for validation.
    """
    print(f"Received value for validation: {value}")
    
    # Supported image extensions and formats
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']
    image_formats = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'tiff']

    # Function to validate individual URLs
    def validate_url(url):
        try:
            # Use Django's built-in URL validator
            URLValidator()(url)  # This will catch invalid URLs early
            
            # Parse the URL
            parsed_url = urlparse(url)
            
            # Check for scheme and netloc
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValidationError(f'{url} is not a valid URL.')
            
            # Check if URL ends with an image extension or has image format in query
            path_lower = parsed_url.path.lower()
            
            # Check file extension
            is_valid_extension = any(path_lower.endswith(ext) for ext in image_extensions)
            
            # Check query parameters for format
            query_params = {}
            if parsed_url.query:
                query_params = dict(param.split('=') for param in parsed_url.query.split('&') if '=' in param)
            
            is_valid_format = query_params.get('fm') in image_formats
            
            # Validate either by extension or query parameter format
            if not (is_valid_extension or is_valid_format):
                raise ValidationError(f'{url} must be an image URL (jpg, jpeg, png, gif, webp, bmp, tiff).')
        
        except ValidationError as e:
            raise e
        except Exception:
            raise ValidationError(f'Invalid URL: {url}')

    # Automatically wrap a single string input into a list
    if isinstance(value, str):
        value = [value]
    
    # Ensure input is a list (can handle empty or None as well)
    if not isinstance(value, (list, tuple)):
        raise ValidationError('Input must be a list/array of URLs or a single URL string.')
    
    # Ensure each URL in the list is a valid string
    for url in value:
        if not isinstance(url, str):
            raise ValidationError(f"Each URL must be a string, but got {type(url)}.")
        print(f"Validating URL: {url}")  # Print URL to check if it's correctly passed
        validate_url(url)

