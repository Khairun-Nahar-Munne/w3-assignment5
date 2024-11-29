import json
from django.core.management.base import BaseCommand
from app.models import Location

class Command(BaseCommand):
    help = 'Generate a sitemap.json file'

    def handle(self, *args, **kwargs):
        sitemap = []
        countries = Location.objects.filter(location_type="country")
        for country in countries:
            data = {
                country.title: country.country_code.lower(),
                "locations": [
                    {state.title: f"{country.country_code.lower()}/{state.title.lower()}"}
                    for state in Location.objects.filter(parent=country)
                ]
            }
            sitemap.append(data)

        with open('sitemap.json', 'w') as f:
            json.dump(sitemap, f, indent=2)
        self.stdout.write(self.style.SUCCESS('Sitemap generated successfully!'))
