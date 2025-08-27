from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'order']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']