from django import forms
from .models import RecyclingRequest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RecyclingRequestForm(forms.ModelForm):
    use_contact_details = forms.BooleanField(required=False)

    class Meta:
        model = RecyclingRequest
        fields = [
            'item_type', 'description', 'condition', 'location', 'category',
            'use_contact_details', 'image'
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Post Request'))

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data['use_contact_details']:
            instance.contact_email = self.user.email
            instance.contact_phone = self.user.phone_number
            instance.contact_address = self.user.address
            instance.contact_city = self.user.city
            instance.contact_province = self.user.province
            instance.contact_postal_code = self.user.postal_code
            instance.contact_country = self.user.country
        if commit:
            instance.save()
        return instance


class RecyclingRequestSearchForm(forms.Form):
    keyword = forms.CharField(required=False)
    category = forms.ChoiceField(choices=[('', 'All')] + RecyclingRequest.CATEGORY_CHOICES, required=False)
    city = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('search', 'Search'))