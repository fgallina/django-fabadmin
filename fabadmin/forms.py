from itertools import chain
from django.utils import simplejson
from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape, escape
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.encoding import smart_unicode


class FabTaskSelectWidget(forms.Select):

    def render_option(self, selected_choices, task):
        value = force_unicode(task.value)
        selected_html = (value in selected_choices) \
                        and u' selected="selected"' or ''
        return u'<option value="%s"%s title="%s" data="%s">%s</option>' % (
            escape(value),
            selected_html,
            force_unicode(escape(task.short_description)),
            escape(force_unicode(simplejson.dumps(task.__dict__))),
            conditional_escape(force_unicode(task.name)))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for task in chain(self.choices, choices):
            output.append(self.render_option(selected_choices, task))
        return u'\n'.join(output)


class FabTaskChoiceField(forms.ChoiceField):
    widget = FabTaskSelectWidget

    def validate(self, value):
        if value in validators.EMPTY_VALUES and self.required:
            raise ValidationError(self.error_messages['required'])
        if value and not self.valid_value(value):
            raise ValidationError(self.error_messages['invalid_choice'] % {'value': value})

    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        for task in self.choices:
            if value == smart_unicode(task.name):
                return True
        return False


class FabfileForm(forms.Form):
    task = FabTaskChoiceField()
    arguments = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        tasks = kwargs.pop('tasks', None)
        super(FabfileForm, self).__init__(*args, **kwargs)
        self.fields['task'].choices = tasks

    def clean_arguments(self):
        cleaned_data = self.cleaned_data
        arguments = cleaned_data['arguments']
        for arg in arguments.split(":"):
            if arg.startswith("<<") and arg.endswith(">>"):
                raise forms.ValidationError("A required argument is missing")
        return arguments
