from django import forms
from .models import Account
class AddAccount(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = "__all__"
        exclude = ['user']
        
        
