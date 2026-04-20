from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from users.forms import AvatarForm, ProfileForm, SignUpForm, UserSettingsForm
from users.models import Profile


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("users:profile")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:profile")
    else:
        form = SignUpForm()

    return render(request, "users/signup.html", {"form": form})


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        avatar_form = AvatarForm(request.POST, request.FILES, instance=profile)
        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(request, _("Profile updated successfully."))
            return redirect("users:profile")

    return render(
        request,
        "users/profile.html",
        {
            "profile": profile,
            "avatar_form": AvatarForm(instance=profile),
        },
    )


@login_required
def profile_settings_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = UserSettingsForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile updated successfully."))
            return redirect("users:profile_settings")
    else:
        user_form = UserSettingsForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "users/profile_settings.html",
        {
            "profile": profile,
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )
