from django import forms
from .models import Order, Drug

class OrderForm(forms.ModelForm):
    drugs = forms.ModelMultipleChoiceField(
        queryset=Drug.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Order
        fields = ['patient_first_name', 'patient_last_name', 'patient_national_code', 'disease_name', 'drugs', 'prescription_note']

class DrugPrescriptionForm(forms.Form):
    drug = forms.ModelChoiceField(queryset=Drug.objects.all(), required=True)
    prescription_instruction = forms.CharField(max_length=255, required=False)
