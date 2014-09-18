from django.template.loader import render_to_string
from form_designer import models

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag , Tag
from django import template
from form_designer.views import process_form
from form_designer.settings import FORM_TEMPLATES

register = template.Library()

class FormDefinitionTag(Tag):
    name = 'formdefinition'
    options = Options(
        Argument('form_name', required=True,),
        Argument('template_name', required=False,),
    )

    def render_tag(self, context, form_name,template_name):
        form = models.FormDefinition
        form_definition = form.objects.all()[0]
        template = form_definition.form_template_name
        data =  process_form(context['request'], form_definition, context, disable_redirection=True)
        if template_name:
            template = [key for key, value in dict(FORM_TEMPLATES).iteritems() if value == template_name][0]
        output = render_to_string(template, data)
        return output


register.tag(FormDefinitionTag)

