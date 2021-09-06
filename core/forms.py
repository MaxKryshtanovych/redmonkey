from django import forms
from .models import Client, Employer, Check


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = '__all__'


class CheckForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = '__all__'
