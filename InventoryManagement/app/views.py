from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import PropertyOwnerSignupForm


def property_owner_signup(request):
    if request.method == "POST":
        form = PropertyOwnerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Get or create the Property Owners group
            group, created = Group.objects.get_or_create(name="Property Owners")

            # Add the user to the Property Owners group
            user.groups.add(group)

            # Assign permissions to the user if necessary (optional in this case since group already has them)
            group_permissions = group.permissions.all()
            for perm in group_permissions:
                user.user_permissions.add(perm)

            user.save()  # Don't forget to save the user after adding permissions

            messages.success(request, "Your request has been submitted successfully!")
            return redirect("index")  # Replace 'index' with your desired redirect URL
    else:
        form = PropertyOwnerSignupForm()
    return render(request, "signup.html", {"form": form})


def index(request):
    return HttpResponse("Home Page")
