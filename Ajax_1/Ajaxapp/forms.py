from django import forms
from .models import Ajax_data


class AjaxForm(forms.ModelForm):
    # name = forms.CharField(max_length=255)
    # age = forms.IntegerField()

    class Meta:
        model = Ajax_data
        fields = "__all__"
