# -*- encoding: utf-8 -*-

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.forms import ValidationError


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    # def clean_email(self, email):
    #     if not email.endswith("@nimr.or.tz"):
    #         raise ValidationError(
    #             "You must register using your official email address ending with @nimr.or.tz."
    #         )

    def send_mail(self, template_prefix, email, context):
        context["activate_url"] = (
            settings.PUBLIC_URL + "/accounts/confirm-email/" + context["key"] + "/"
        )
        message = self.render_mail(template_prefix, email, context)
        message.send()
