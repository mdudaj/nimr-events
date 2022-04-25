# -*- encoding: utf-8 -*-

from django import forms


class PropellerCheckboxInput(forms.CheckboxInput):
    """CheckboxInput using propellerkit theme."""

    template_name = "widgets/propeller_checkbox.html"
