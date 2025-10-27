from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['p_pic', 'bio']

        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': "Escreva um pouco sobre você..."}),
        }