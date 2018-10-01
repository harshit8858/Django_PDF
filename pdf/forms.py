from django import forms
from .models import *


class PdfForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = [
            'title',
            'data',
        ]
