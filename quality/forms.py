from django import forms
from .models import ProductionJob, QualityInspection


class ProductionJobForm(forms.ModelForm):
    class Meta:
        model = ProductionJob
        fields = [
            'part_number',
            'part_name',
            'quantity',
            'status',
        ]
        widgets = {
            'part_number': forms.TextInput(attrs={
                'placeholder': 'e.g. SHAFT-001'
            }),
            'part_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Steel Shaft'
            }),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError(
                'Quantity must be at least 1.'
            )
        return quantity


class QualityInspectionForm(forms.ModelForm):
    class Meta:
        model = QualityInspection
        fields = [
            'job',
            'actual_measurement',
            'min_tolerance',
            'max_tolerance',
            'is_final',
            'remarks',
        ]
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        minimum = cleaned_data.get('min_tolerance')
        maximum = cleaned_data.get('max_tolerance')

        if minimum is not None and maximum is not None:
            if minimum > maximum:
                raise forms.ValidationError(
                    'Minimum tolerance cannot exceed maximum tolerance.'
                )

        return cleaned_data
