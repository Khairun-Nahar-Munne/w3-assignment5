from django.test import TestCase
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from .models import Accommodation, Location, User
from unittest.mock import patch
from langdetect import detect
from django.contrib.auth.models import User
class LocationModelTest(TestCase):
    def setUp(self):
        # Set up test data for the Location model
        self.location_1 = Location.objects.create(
            id="loc001",
            title="Location 1",
            center=Point(1.0, 1.0),
            location_type="Type A",
            country_code="US",
            state_abbr="CA",
            city="Los Angeles"
        )
        self.location_2 = Location.objects.create(
            id="loc002",
            title="Location 2",
            center=Point(2.0, 2.0),
            location_type="Type B",
            country_code="US",
            state_abbr="NY",
            city="New York",
            parent=self.location_1  # Set parent-child relationship
        )

    def test_location_creation(self):
        # Check that location 1 is created correctly
        location = self.location_1
        self.assertEqual(location.id, "loc001")
        self.assertEqual(location.title, "Location 1")
        self.assertEqual(location.center.x, 1.0)  # Check coordinates of the point
        self.assertEqual(location.center.y, 1.0)
        self.assertEqual(location.location_type, "Type A")
        self.assertEqual(location.country_code, "US")
        self.assertEqual(location.state_abbr, "CA")
        self.assertEqual(location.city, "Los Angeles")
    
    def test_location_parent_relationship(self):
        # Test the parent-child relationship
        location = self.location_2
        self.assertEqual(location.parent, self.location_1)

    def test_location_str_method(self):
        # Test the __str__ method
        location = self.location_1
        self.assertEqual(str(location), "Location 1")

    def test_location_field_blank_null(self):
        # Test that the city and state_abbr fields can be blank or null
        location = Location.objects.create(
            id="loc003",
            title="Location 3",
            center=Point(3.0, 3.0),
            location_type="Type C",
            country_code="CA",
            state_abbr=None,  # Test with null value
            city=None          # Test with blank value
        )
        self.assertIsNone(location.state_abbr)
        self.assertIsNone(location.city)

    def test_location_update(self):
        # Test the auto update functionality of the updated_at field
        location = self.location_1
        original_updated_at = location.updated_at
        location.title = "Updated Location"
        location.save()
        self.assertNotEqual(location.updated_at, original_updated_at)  # Check that updated_at is updated

class AccommodationModelTest(TestCase):
    def setUp(self):
        # Set up test data for the Location and User models
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
        self.location2 = Location.objects.create(
            id="loc002",
            title="Location 2",
            center=Point(2.0, 2.0),
            location_type="Type B",
            country_code="US",
            state_abbr="NY",
            city="New York"
        )

    def test_accommodation_creation(self):
        # Test creating an accommodation
        accommodation = Accommodation.objects.create(
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
        self.assertEqual(accommodation.title, "Test Accommodation")
        self.assertEqual(accommodation.country_code, "US")
        self.assertEqual(accommodation.bedroom_count, 2)
        self.assertEqual(accommodation.review_score, 4.5)
        self.assertEqual(accommodation.usd_rate, 100.00)
        self.assertEqual(accommodation.location, self.location)
        self.assertEqual(accommodation.user, self.user)
        self.assertIn("WiFi", accommodation.amenities)
        self.assertIn("Air Conditioning", accommodation.amenities)

    def test_amenities_validation(self):
        # Test that amenities validation works correctly
        valid_amenities = ["WiFi", "Air Conditioning"]
        accommodation = Accommodation(
            id="acc002",
            title="Another Test Accommodation",
            country_code="US",
            bedroom_count=3,
            review_score=4.0,
            usd_rate=120.00,
            center=Point(2.0, 2.0),
            location=self.location,
            user=self.user,
            amenities=valid_amenities
        )
        try:
            accommodation.full_clean()  # This will run the clean method and validators
        except ValidationError:
            self.fail("Accommodation with valid amenities should not raise ValidationError.")

        # Test that an amenity that exceeds 100 characters is invalid
        long_amenity = "A" * 101
        invalid_amenities = ["WiFi", long_amenity]
        accommodation.amenities = invalid_amenities
        with self.assertRaises(ValidationError):
            accommodation.full_clean()

  
   
    def test_location_country_code_mismatch(self):
        # Test that a validation error is raised when country_code doesn't match the location's country code
        accommodation = Accommodation(
            id="acc006",
            title="Accommodation with Mismatched Location Country Code",
            country_code="CA",  # Mismatched country code
            bedroom_count=2,
            review_score=3.5,
            usd_rate=180.00,
            center=Point(2.0, 2.0),
            location=self.location2,  # Location with country_code="US"
            user=self.user,
            amenities=["WiFi"],
        )
        with self.assertRaises(ValidationError):
            accommodation.full_clean()



