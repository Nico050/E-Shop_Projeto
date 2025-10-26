from django import forms
from .models import Reviews

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(1, '1★'), (2, '2★'), (3, '3★'), (4, '4★'), (5, '5★')], widget=forms.RadioSelect, label='Sua nota')

    class Meta:
        model = Reviews
        fields = ['rating', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }