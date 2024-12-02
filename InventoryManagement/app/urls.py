from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', views.property_owner_signup, name='property_owner_signup'),
]