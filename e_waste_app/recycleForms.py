from django import forms
from .models import RecyclingRequest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RecyclingRequestForm(forms.ModelForm):
    user_profile_contact = forms.BooleanField(initial=False, required=False,
                                              label="Use contact details from my profile (Leave the next fields blank "
                                                    "if you choose this option)")

    class Meta:
        model = RecyclingRequest
        fields = [
            'item_type', 'description', 'condition', 'category',
            'image', 'phone', 'address', 'city', 'province', 'postal_code', 'country'
        ]

    def __init__(self, *args, **kwargs):
        super(RecyclingRequestForm, self).__init__(*args, **kwargs)

        # Reorder fields
        self.fields['user_profile_contact'] = self.fields.pop('user_profile_contact')
        fields_order = [
            'item_type',
            'description',
            'condition',
            'category',
            'image',
            'user_profile_contact',
            'phone', 'address', 'city', 'province', 'postal_code', 'country'
        ]
        self.order_fields(fields_order)


class RecyclingRequestSearchForm(forms.Form):
    keyword = forms.CharField(required=False)
    category = forms.ChoiceField(choices=[('', 'All')] + RecyclingRequest.CATEGORY_CHOICES, required=False)
    city = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('search', 'Search'))