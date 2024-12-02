from django.core.management.base import BaseCommand
from app.models import Location
from django.utils.text import slugify
import json

class Command(BaseCommand):
    help = 'Generate a sitemap.json for all country locations'

    def handle(self, *args, **kwargs):
        # Fetch all locations sorted alphabetically by title
        locations = Location.objects.all().order_by('title')

        # Dictionary to store the country and its locations
        sitemap_data = {}

        # Debug: Check if locations are being retrieved correctly
        print(f"Found {locations.count()} locations")

        # Iterate over all locations
        for location in locations:
            print(f"Processing Location: {location.title} of type {location.location_type}")

            # Handle 'country' type location (top-level)
            if location.location_type == 'country':
                country_slug = slugify(location.title)  # Generate slug dynamically
                country_title = location.title
                if country_slug not in sitemap_data:
                    sitemap_data[country_slug] = {
                        "name": country_title,
                        "locations": []
                    }

                # Debug: Print the country and its slug
                print(f"Adding country: {country_title} with slug: {country_slug}")

            # Handle 'state', 'city', or 'Urban' locations (nested under countries)
            elif location.location_type in ['state', 'city', 'Urban']:
                parent_location = location.parent
                if parent_location and parent_location.location_type == 'country':
                    country_slug = slugify(parent_location.title)  # Generate slug dynamically
                    location_slug = slugify(location.title)  # Generate slug dynamically
                    location_url = f"{country_slug}/{location_slug}"

                    # Add state/city/urban location to its country's location list
                    if country_slug in sitemap_data:
                        sitemap_data[country_slug]["locations"].append({
                            location.title: location_url
                        })
                    # Debug: Print the location (state/city/urban) and its URL
                    print(f"Adding location: {location.title} under {country_slug} with URL: {location_url}")

        # Debug: Print the entire sitemap_data to see the content
        print("Sitemap data collected:", sitemap_data)

        # Sort locations alphabetically by location name
        for country, data in sitemap_data.items():
            data["locations"] = sorted(data["locations"], key=lambda x: list(x.keys())[0])

        # Save the generated data to a JSON file
        with open('sitemap.json', 'w') as json_file:
            json.dump(sitemap_data, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS("Sitemap generated successfully!"))
