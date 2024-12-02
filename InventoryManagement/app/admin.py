from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, LocalizeAccommodation
import csv
from django.http import HttpResponse
from django.contrib import messages
from io import StringIO
from django.urls import path, reverse
from django.shortcuts import redirect, render
from io import StringIO
from guardian.shortcuts import get_objects_for_user
from django.utils.html import format_html


@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = (
        "id",
        "title",
        "location_type",
        "country_code",
        "state_abbr",
        "city",
    )
    search_fields = ("title", "location_type", "country_code")
    list_filter = ("location_type",)

    def changelist_view(self, request, extra_context=None):
        """
        Add a custom "Import CSV" button to the changelist view.
        """
        extra_context = extra_context or {}
        extra_context["import_csv_url"] = reverse("admin:import_locations_csv")
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-csv/", self.import_csv_view, name="import_locations_csv"),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        if request.method == "POST" and "csv_file" in request.FILES:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith(".csv"):
                self.message_user(
                    request, "Please upload a valid CSV file.", level=messages.ERROR
                )
                return self.render_csv_import_form(request)

            try:
                file_data = StringIO(csv_file.read().decode("utf-8"))
                reader = csv.reader(file_data)
                next(reader)  # Skip header row
                for row in reader:
                    if row:
                        parent = None
                        if row[3]:  # Check if parent_id is provided (column 4)
                            parent = Location.objects.filter(id=row[3]).first()

                        # Ensure state_abbr is None if it's empty in the CSV
                        state_abbr = row[6] if row[6] else None

                        Location.objects.create(
                            id=row[0],
                            title=row[1],
                            center=row[2],  # Parse the point correctly
                            parent=parent,  # Assign the parent location
                            location_type=row[4],
                            country_code=row[5],
                            state_abbr=state_abbr,
                            city=row[7] if row[7] else None,
                        )
                self.message_user(
                    request, "Locations imported successfully.", level=messages.SUCCESS
                )
                return redirect("admin:app_location_changelist")
            except Exception as e:
                self.message_user(
                    request, f"Error importing CSV: {e}", level=messages.ERROR
                )
        return self.render_csv_import_form(request)



    def render_csv_import_form(self, request):
        opts = Location._meta
        return render(request, "admin/csv_import_form.html", context={"opts": opts})


@admin.register(Accommodation)
class AccommodationAdmin(LeafletGeoAdmin):
    list_display = ("id", "title", "user", "location", "bedroom_count", "published")
    search_fields = ("title",)
    list_filter = ("published", "location")

    def get_queryset(self, request):
        """
        This method ensures that a property owner can only see their own accommodations.
        """
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            return queryset.filter(user=request.user)
        return queryset

    def save_model(self, request, obj, form, change):
        """
        Ensure that when a property owner creates a new accommodation, it's linked to their user account.
        """
        if not change:  # If it's a new object being created
            obj.user = request.user
        super().save_model(request, obj, form, change)


    settings_overrides = {
        "DEFAULT_CENTER": (0, 0),  # Default center of the map
        "DEFAULT_ZOOM": 3,  # Default zoom level
        "MAX_ZOOM": 18,  # Maximum zoom level
        "SCROLL_ZOOM": True,  # Enable zoom with mouse scroll
        "DRAGGABLE": True,  # Allow panning of the map
        "TOUCH_ZOOM": True,  # Allow pinch zoom on touch devices
    }


@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "language")
    search_fields = ("property__title", "language")
    list_filter = ("language",)
