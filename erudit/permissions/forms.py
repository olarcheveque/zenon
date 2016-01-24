from django import forms

from .models import Rule


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ('user', 'group', 'permission', )

    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)
        prefix = "all:"
        choices = self.fields['permission'].choices
        choices = [item for item in choices if item[0].startswith(prefix)]
        self.fields['permission'].choices = choices
