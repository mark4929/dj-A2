from django import forms
from .models import Bank, Branch

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'swift_code', 'inst_num', 'description']
       

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'transit_num', 'address', 'email', 'capacity']
       