from django.test import TestCase
from django.core.exceptions import ValidationError
from .validators import validate_image_url, validate_images_field

class ImageUrlValidatorTests(TestCase):
    def test_valid_image_urls(self):
        """
        Test that valid image URLs pass the validation
        """
        valid_urls = [
            'https://example.com/image.jpg',
            'http://test.com/path/to/image.png',
            'https://subdomain.example.com/image.gif',
            'http://example.com/image.jpeg',
            'https://example.com/path/image.webp',
            'http://example.com/image.bmp',
            'https://example.com/image.tiff'
        ]
        
        for url in valid_urls:
            try:
                validate_image_url(url)
            except ValidationError:
                self.fail(f"Valid URL {url} raised ValidationError unexpectedly!")

    
        """
        Test that invalid image URLs raise ValidationError
        """
        invalid_urls = [
            # Malformed URLs
            'not a url',
            'httpx://invalid.url',
            
            # URLs without image extensions
            'https://example.com/document.pdf',
            'http://example.com/file.txt',
            
            # URLs with incorrect file extensions
            'https://example.com/image.jpx',
            'http://example.com/image.pngg',
            
            # URLs with image-like extensions in the middle of the path
            'https://example.com/file.jpg/not-an-image',
            'http://example.com/path.png/something'
        ]
        
        for url in invalid_urls:
            with self.assertRaises(ValidationError, 
                                   msg=f"URL {url} should have raised ValidationError"):
                validate_image_url(url)

    def test_validate_images_field_valid(self):
        """
        Test validate_images_field with valid list of image URLs
        """
        valid_image_list = [
            'https://example.com/image1.jpg',
            'http://test.com/image2.png',
            'https://example.com/image3.gif'
        ]
        
        try:
            validate_images_field(valid_image_list)
        except ValidationError:
            self.fail("Valid image list raised ValidationError unexpectedly!")

    
    def test_validate_images_field_with_invalid_urls(self):
        """
        Test validate_images_field with a list containing invalid URLs
        """
        invalid_url_list = [
            'https://example.com/image1.jpg',
            'not a valid url',
            'http://example.com/document.pdf'
        ]
        
        with self.assertRaises(ValidationError, 
                               msg="List with invalid URLs should have raised ValidationError"):
            validate_images_field(invalid_url_list)

    def test_validate_images_field_empty_input(self):
        """
        Test validate_images_field with empty input
        """
        try:
            validate_images_field([])
            validate_images_field(None)
        except ValidationError:
            self.fail("Empty input should not raise ValidationError")