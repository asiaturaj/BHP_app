from django import forms
from .models import ProtectiveClothingSet, Employee


class ReleaseForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.filter(obtained_set__isnull=True), label="Pracownik")
    pc_set = forms.ModelChoiceField(queryset=ProtectiveClothingSet.objects.all(), label="Zestaw do wydania")