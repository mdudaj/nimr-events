# -*- encoding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import PersonManager


class TimeStampedModel(models.Model):
    """Abstract class that includes timestamp fields."""

    created = models.DateTimeField(
        verbose_name=_("Created"),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name=_("Modified"),
        auto_now=True,
    )

    class Meta:
        """Meta options for TimeStampedModel."""

        abstract = True


class Country(TimeStampedModel, models.Model):
    """Model class for country information."""

    name = models.CharField(
        _("Name"),
        max_length=512,
    )

    class Meta:
        abstract = False
        db_table = "Country"
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Institution(TimeStampedModel, models.Model):
    """Affiliated Institution."""

    name = models.CharField(
        _("Name"),
        max_length=1024,
    )
    country = models.ForeignKey(
        Country,
        verbose_name=_("Country"),
        on_delete=models.CASCADE,
    )
    address = models.CharField(
        _("Address"),
        max_length=1024,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = False
        db_table = "Institution"
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")
        ordering = [
            "name",
            "country",
        ]

    def __str__(self):
        return "{} - {}".format(self.name, self.country)


class Person(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    """Participants'  information model."""

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

    prefix = models.CharField(
        _("Prefix"),
        max_length=4,
        choices=PREFIX_CHOICES,
    )
    first_name = models.CharField(
        _("First Name"),
        max_length=255,
    )
    middle_name = models.CharField(
        _("Middle Name"),
        max_length=255,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=255,
    )
    sex = models.CharField(
        _("Sex"),
        choices=SEX_CHOICES,
        max_length=1,
        default=NOT_KNOWN,
        null=True,
    )
    institution = models.ForeignKey(
        Institution,
        verbose_name=_("Institution"),
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        _("Email address"),
        unique=True,
    )
    phone = PhoneNumberField(
        _("Phone"),
    )
    registration_type = models.CharField(
        _("Registration Type"),
        choices=REGISTRATION_CHOICES,
        max_length=11,
    )

    # app related
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    objects = PersonManager()

    class Meta:
        abstract = False
        db_table = "Person"
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        ordering = [
            "first_name",
            "last_name",
            "created",
        ]

    def get_name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("registration:person-detail", kwargs={"pk": self.pk})


class Exhibitor(TimeStampedModel, models.Model):
    """Exhibitors' information model."""

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
    )
    booths = models.IntegerField(_("Number of Booths"), null=False)
    personnel = models.ManyToManyField(
        Person,
        verbose_name=_("Participant(s)"),
        related_name="personnel",
        through="ExhibitorPersonnel",
    )

    class Meta:
        abstract = False
        db_table = "Exhibitor"
        verbose_name = _("Exhibitor")
        verbose_name_plural = _("Exhibitors")
        ordering = [
            "institution",
            "booths",
        ]

    def __str__(self):
        return self.institution

    def get_absolute_url(self):
        return reverse("registration:exhibitor-detail", kwargs={"pk": self.pk})


class ExhibitorPersonnel(TimeStampedModel, models.Model):
    """Exhibitors' participants information model."""

    institution = models.ForeignKey(
        Exhibitor,
        verbose_name=_("Institution"),
        on_delete=models.CASCADE,
    )
    participant = models.ForeignKey(
        Person,
        verbose_name=_("Participant"),
        on_delete=models.CASCADE,
    )
    contact = models.BooleanField(_("Contact Person?"), default=False)

    class Meta:
        abstract = False
        db_table = "ExhibitorPersonnel"
        ordering = [
            "participant",
        ]

    def __str__(self):
        return self.participant


class AwardNominee(TimeStampedModel, models.Model):
    """Awards' Nominee information model."""

    # Award choices
    AWARD_CHOICES = (
        ("Maria Kamm Best Female Scientist Award", _("Maria Kamm Best Female Scientist Award")),
        ("Mwelecele Malecela Memorial Award", _("Mwelecele Malecela Memorial Award")),
        (
            "The National Best Health Scientist Award",
            _("The National Best Health Scientist Award"),
        ),
        ("The National Health Innovation Award", _("The National Health Innovation Award")),
        (
            "The National Lifetime Award in Health Research",
            _("The National Lifetime Award in Health Research"),
        ),
        ("The NIMR Best Scientist Award", _("The NIMR Best Scientist Award")),
    )

    nominee = models.ForeignKey(
        Person,
        verbose_name=_("Nominee"),
        related_name="nominees",
        on_delete=models.CASCADE,
    )
    award = models.CharField(
        _("Award"),
        choices=AWARD_CHOICES,
        max_length=50,
    )
    votes = models.IntegerField(
        _("Votes"),
        default=0,
    )
    voters = models.ManyToManyField(
        Person,
        related_name="voters",
    )

    class Meta:
        abstract = False
        db_table = "AwardNominee"

    def __str__(self):
        return self.nominee

    def get_absolute_url(self):
        return reverse("registration:nominee-detail", kwargs={"pk": self.pk})
