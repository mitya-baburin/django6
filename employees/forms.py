from django import forms
from .models import Employee, Image  
from .models import Image

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['username', 'password', 'gender', 'skills', 'hire_date']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Это поле обязательно.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Это поле обязательно.")
        return password

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'order'] 

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']