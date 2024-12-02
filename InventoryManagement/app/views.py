from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import PropertyOwnerSignupForm
from guardian.shortcuts import get_objects_for_user
from django.shortcuts import get_object_or_404
from .models import Accommodation


def view_accommodation(request, pk):
    accommodation = get_object_or_404(
        get_objects_for_user(request.user, "view_accommodation", klass=Accommodation),
        pk=pk,
    )
    return render(
        request, "accommodation_detail.html", {"accommodation": accommodation}
    )


def edit_accommodation(request, pk):
    accommodation = get_object_or_404(
        get_objects_for_user(request.user, "change_accommodation", klass=Accommodation),
        pk=pk,
    )
    # Handle editing logic
    return render(request, "accommodation_edit.html", {"accommodation": accommodation})


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
    return HttpResponse("Successfully Signed Up!")
