# -*- encoding: utf-8 -*-

from sys import prefix

from allauth.account import forms as authforms
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import AwardNominee, Exhibitor, ExhibitorPersonnel, Institution, Person


class ChangePasswordForm(authforms.ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "placeholder": "",
                    "class": "form-control",
                }
            )


class ResetPasswordForm(authforms.ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "placeholder": "",
                    "class": "form-control",
                }
            )


class ResetPasswordForm(authforms.ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "placeholder": "",
                    "class": "form-control",
                }
            )


class LoginForm(authforms.LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "placeholder": "",
                    "class": "form-control",
                }
            )


class SignupForm(authforms.SignupForm):
    # sex choices
    # according to https://en.wikipedia.org/wiki/ISO/IEC_5218
    NOT_KNOWN = "0"
    MALE = "1"
    FEMALE = "2"
    NOT_APPLICABLE = "9"

    SEX_CHOICES = (
        (NOT_KNOWN, _("Not Known")),
        (MALE, _("Male")),
        (FEMALE, _("Female")),
        (NOT_APPLICABLE, _("Not Applicable")),
    )

    # Prefix choices
    PROF = "PROF"
    DR = "DR"
    MR = "MR"
    MRS = "MRS"
    MS = "MS"
    REV = "REV"

    PREFIX_CHOICES = (
        (PROF, _("Prof.")),
        (DR, _("Dr.")),
        (MR, _("Mr.")),
        (MRS, _("Mrs.")),
        (MS, _("Ms.")),
        (REV, _("REV")),
    )

    # Registration choices
    ORGANIZER = "ORGANIZER"
    PRESENTER = "PRESENTER"
    EXHIBITOR = "EXHIBITOR"
    PARTICIPANT = "PARTICIPANT"
    STUDENT = "STUDENT"

    REGISTRATION_CHOICES = (
        (ORGANIZER, _("Organizer")),
        (PRESENTER, _("Presenter")),
        (EXHIBITOR, _("Exhibitor")),
        (PARTICIPANT, _("Participant")),
        (STUDENT, _("Student")),
    )

    prefix = forms.ChoiceField(
        label=_("Prefix"),
        choices=PREFIX_CHOICES,
        max_length=4,
    )
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=255,
    )
    middle_name = forms.CharField(
        label=_("Middle Name"),
        max_length=4,
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=255,
    )
    sex = forms.CharField(
        label=_("Sex"),
        choices=SEX_CHOICES,
        max_length=1,
        default=NOT_KNOWN,
    )
    institution = forms.ChoiceField(
        label=_("Institution"),
        max_length=10,
        choices=Institution.objects.all(),
    )
    phone = forms.CharField(
        label=_("Phone"),
        max_length=14,
    )
    registration_type = forms.CharField(
        label=_("Registration Type"),
        choices=REGISTRATION_CHOICES,
        max_length=11,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "placeholder": "",
                    "class": "form-control",
                }
            )

    def save(self, request):
        user = super().save(request)
        user.prefix = self.cleaned_data["prefix"]
        user.first_name = self.cleaned_data["first_name"]
        user.middle_name = self.cleaned_data["middle_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.sex = self.cleaned_data["sex"]
        user.institution = self.cleaned_data["institution"]
        user.phone = self.cleaned_data["phone"]
        user.registration_type = self.cleaned_data["registration_type"]

        user.save()
        return user
