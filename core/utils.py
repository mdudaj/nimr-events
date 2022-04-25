# -*- encoding: utf-8 -*-

from datetime import datetime
from ensurepip import bootstrap

import weasyprint
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration


def render_to_pdf(template_name, filename, report_css_path, context_dict={}):
    html = render_to_string(template_name, context_dict)
    response = HttpResponse(content_type="application/pdf")
    response["content-disposition"] = "inline; filename={name}-{date}.pdf".format(
        name=filename, date=datetime.now().date().strftime("%Y-%m-%d")
    )

    bootstrap4_css = settings.STATIC_ROOT + "/assets/css/bootstrap4-admin-compress.min.css"
    report_css = settings.STATIC_ROOT + report_css_path
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(
        response,
        font_config=font_config,
        stylesheets=[CSS(bootstrap4_css), CSS(report_css)],
    )
    return response
