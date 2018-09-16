from django import forms

from .models import LinkStore


class URLForm(forms.ModelForm):
    class Meta:
        model = LinkStore
        fields = ('link', 'description', 'status')