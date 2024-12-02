from django.core.management.base import BaseCommand
from app.models import Location
from django.utils.text import slugify
import json

class Command(BaseCommand):
    help = 'Generate a sitemap.json for all locations'

    def handle(self, *args, **kwargs):
        # Fetch all locations sorted alphabetically by title
        locations = Location.objects.all().order_by('title')

        # Dictionary to store the country and its locations
        sitemap_data = {}

        # Iterate over all locations
        for location in locations:
            # Handle 'country' type location (top-level)
            if location.location_type == 'country':
                country_slug = slugify(location.title)
                if country_slug not in sitemap_data:
                    sitemap_data[country_slug] = {
                        "name": location.title,
                        "locations": []
                    }

            # Handle 'state' locations (under countries)
            elif location.location_type == 'state':
                parent_location = location.parent
                if parent_location and parent_location.location_type == 'country':
                    country_slug = slugify(parent_location.title)
                    state_slug = slugify(location.title)
                    state_url = f"{country_slug}/{state_slug}"
                    
                    if country_slug in sitemap_data:
                        state_entry = {
                            state_slug: {
                                "name": location.title,
                                "locations": []
                            }
                        }
                        sitemap_data[country_slug]["locations"].append(state_entry)

            # Handle 'city' locations (under states)
            elif location.location_type == 'city':
                parent_location = location.parent
                if parent_location and parent_location.location_type == 'state':
                    country_location = parent_location.parent
                    if country_location and country_location.location_type == 'country':
                        country_slug = slugify(country_location.title)
                        state_slug = slugify(parent_location.title)
                        city_slug = slugify(location.title)
                        city_url = f"{country_slug}/{state_slug}/{city_slug}"
                        
                        # Find the correct country in sitemap_data
                        for country_entry in sitemap_data.get(country_slug, {}).get("locations", []):
                            for state_key, state_data in country_entry.items():
                                if state_key == state_slug:
                                    # Add city to the state's locations
                                    state_data.setdefault("locations", []).append({
                                        city_slug: {
                                            "name": location.title,
                                            "url": city_url
                                        }
                                    })
                                    break

        # Sort locations alphabetically
        for country, data in sitemap_data.items():
            data["locations"] = sorted(data["locations"], key=lambda x: list(x.keys())[0])
            for state_entry in data["locations"]:
                for state_data in state_entry.values():
                    if "locations" in state_data:
                        state_data["locations"] = sorted(
                            state_data["locations"], 
                            key=lambda x: list(x.keys())[0]
                        )

        # Save the generated data to a JSON file
        with open('sitemap.json', 'w') as json_file:
            json.dump(sitemap_data, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS("Sitemap generated successfully!"))