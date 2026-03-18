from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Crop, FarmerQuery, ExpertResponse

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_name', 'category', 'season', 'soil_type', 'fertilizer', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class FarmerQueryForm(forms.ModelForm):
    class Meta:
        model = FarmerQuery
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3}),
        }

class ExpertResponseForm(forms.ModelForm):
    class Meta:
        model = ExpertResponse
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={'rows': 5}),
        }
