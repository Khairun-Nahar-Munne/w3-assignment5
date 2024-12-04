from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.gis.geos import Point
from .models import LocalizeAccommodation, Accommodation, Location, User
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

class LocalizeAccommodationModelTests(TestCase):
    def setUp(self):
        # Create a base accommodation for testing
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.location = Location.objects.create(
            id="loc001",
            title="Location 1",
            center=Point(1.0, 1.0),
            location_type="Type A",
            country_code="US",
            state_abbr="CA",
            city="Los Angeles"
        )
        self.accommodation = Accommodation.objects.create(
            id="acc001",
            title="Test Accommodation",
            country_code="US",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=100.00,
            center=Point(1.0, 1.0),
            location=self.location,
            user=self.user,
            amenities=["WiFi", "Air Conditioning"],
        )
      

    def test_valid_description_language_match(self):
        """
        Test that a description in the correct language passes validation
        """
        localize_accommodation = LocalizeAccommodation(
            property=self.accommodation,
            language='en',
            description='This is a beautiful apartment in the city center.',
            policy={'cancellation': 'Free cancellation up to 24 hours before check-in'}
        )
        
        try:
            localize_accommodation.full_clean()
        except ValidationError:
            self.fail('Validation should pass for matching language description')

    

    def test_policy_language_match(self):
        """
        Test that policy text is in the same language as specified
        """
        localize_accommodation = LocalizeAccommodation(
            property=self.accommodation,
            language='es',
            description='Este es un hermoso apartamento en el centro de la ciudad.',
            policy={'cancellation': 'Cancelación gratuita hasta 24 horas antes del check-in'}
        )
        
        try:
            localize_accommodation.full_clean()
        except ValidationError:
            self.fail('Policy text in matching language should pass validation')

    def test_policy_language_mismatch(self):
        """
        Test that a policy text in a different language raises a ValidationError
        """
        localize_accommodation = LocalizeAccommodation(
            property=self.accommodation,
            language='de',
            description='Dies ist eine wunderschöne Wohnung im Stadtzentrum.',
            policy={'cancellation': 'Free cancellation policy'}  # English policy
        )
        
        with self.assertRaises(ValidationError):
            localize_accommodation.full_clean()

    
    def test_multiple_policy_entries(self):
        """
        Test validation with multiple policy entries
        """
        localize_accommodation = LocalizeAccommodation(
            property=self.accommodation,
            language='pt',
            description='Este é um apartamento lindo no centro da cidade.',
            policy={
                'cancellation': 'Cancelamento gratuito até 24 horas antes do check-in',
                'pets': 'Animais de estimação são permitidos'
            }
        )
        
        try:
            localize_accommodation.full_clean()
        except ValidationError:
            self.fail('Multiple policy entries in the same language should pass validation')

    