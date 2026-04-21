from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

from users.models import Profile

UserModel = get_user_model()


class StyledFieldsMixin:
    text_input_classes = "form-control"
    select_classes = "form-select"
    checkbox_classes = "form-check-input"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css_classes = self.checkbox_classes
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css_classes = self.select_classes
            else:
                css_classes = self.text_input_classes

            existing_classes = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing_classes} {css_classes}".strip()


class EmailOrUsernameAuthenticationForm(StyledFieldsMixin, AuthenticationForm):
    username = forms.CharField(
        label=_("Username or email"),
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": _("chef or chef@example.com"),
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": _("Enter your password"),
            }
        ),
    )


class SignUpForm(StyledFieldsMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": _("Choose a username"),
            "email": _("chef@example.com"),
            "first_name": _("Your first name"),
            "last_name": _("Your last name"),
            "password1": _("Create a strong password"),
            "password2": _("Repeat the password"),
        }
        for name, placeholder in placeholders.items():
            self.fields[name].widget.attrs.setdefault(
                "placeholder", placeholder
            )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if UserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                _("A user with this email already exists.")
            )
        return email


class PasswordResetRequestForm(StyledFieldsMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.setdefault(
            "placeholder", _("chef@example.com")
        )


class UserProfileForm(StyledFieldsMixin, forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("instance")
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.setdefault(
            "placeholder", _("chefmaster")
        )
        self.fields["email"].widget.attrs.setdefault(
            "placeholder", _("chef@example.com")
        )
        self.fields["first_name"].widget.attrs.setdefault(
            "placeholder", _("Anna")
        )
        self.fields["last_name"].widget.attrs.setdefault(
            "placeholder", _("Ivanova")
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        queryset = UserModel.objects.filter(email__iexact=email)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError(
                _("A user with this email already exists.")
            )
        return email

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        queryset = UserModel.objects.filter(username__iexact=username)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError(
                _("A user with this username already exists.")
            )
        return username


class UserSettingsForm(StyledFieldsMixin, forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        queryset = UserModel.objects.filter(email__iexact=email)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError(
                _("A user with this email already exists.")
            )
        return email

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        queryset = UserModel.objects.filter(username__iexact=username)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError(
                _("A user with this username already exists.")
            )
        return username


class ProfileForm(StyledFieldsMixin, forms.ModelForm):
    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Profile
        fields = ("birthday", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs["class"] = "form-control"
        min_birthday = self.get_min_birthday()
        max_birthday = date.today()
        self.fields["birthday"].widget.attrs["min"] = min_birthday.isoformat()
        self.fields["birthday"].widget.attrs["max"] = max_birthday.isoformat()

    @staticmethod
    def get_min_birthday():
        today = date.today()
        try:
            return today.replace(year=today.year - 120)
        except ValueError:
            return today.replace(month=2, day=28, year=today.year - 120)

    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if not birthday:
            return birthday

        today = date.today()
        min_birthday = self.get_min_birthday()

        if birthday > today:
            raise forms.ValidationError(_("Birthday cannot be in the future."))
        if birthday < min_birthday:
            raise forms.ValidationError(
                _("Please enter a realistic date of birth.")
            )
        return birthday


class AvatarForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "id": "id_image",
                "accept": "image/*",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ("image",)
