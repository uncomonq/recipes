from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from users.forms import ProfileForm, SignUpForm, UserSettingsForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("users:profile")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Account created successfully."))
            return redirect("users:profile")
    else:
        form = SignUpForm()

    return render(request, "users/signup.html", {"form": form})


@login_required
def profile_view(request):
    return render(
        request,
        "users/profile.html",
        {
            "profile": request.user.profile,
        },
    )


@login_required
def profile_settings_view(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        user_form = UserSettingsForm(request.POST, instance=user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile updated successfully."))
            return redirect("users:profile")
    else:
        user_form = UserSettingsForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "users/profile_settings.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )
