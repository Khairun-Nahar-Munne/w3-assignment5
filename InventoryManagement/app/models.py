from django.db import models
from django.contrib.gis.db import models as geomodels

class Location(models.Model):
    # ID field
    id = models.CharField(max_length=20, primary_key=True)
    
    # Name field
    title = models.CharField(max_length=100)
    
    # Geolocation field using PostGIS point
    center = geomodels.PointField()
    
    # Hierarchical Location - Foreign key to self
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    
    # Type of location (continent, country, state, city, etc.)
    location_type = models.CharField(max_length=20)
    
    # ISO country code
    country_code = models.CharField(max_length=2)
    
    # State abbreviation (only for states)
    state_abbr = models.CharField(max_length=3, null=True, blank=True)
    
    # City name
    city = models.CharField(max_length=30, null=True, blank=True)
    
    # Timestamps for creation and updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
