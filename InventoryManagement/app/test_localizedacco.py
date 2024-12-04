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

    

    