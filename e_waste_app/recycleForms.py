from django import forms
from .models import RecycleItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AddRecycleItemForm(forms.ModelForm):
    user_profile_contact = forms.BooleanField(initial=False, required=False,
                                              label="Use contact details from my profile (Leave the next fields blank "
                                                    "if you choose this option)")

    class Meta:
        model = RecycleItem
        fields = [
            'item_type', 'description', 'condition', 'category',
            'image', 'phone_number', 'email', 'address', 'city', 'province', 'postal_code', 'country'
        ]

    def __init__(self, *args, **kwargs):
        super(AddRecycleItemForm, self).__init__(*args, **kwargs)

        # Reorder fields
        self.fields['user_profile_contact'] = self.fields.pop('user_profile_contact')
        fields_order = [
            'item_type',
            'description',
            'condition',
            'category',
            'image',
            'user_profile_contact',
            'phone_number', 'email', 'address', 'city', 'province', 'postal_code', 'country'
        ]
        self.order_fields(fields_order)


class SearchRecycleItemsForm(forms.Form):
    keyword = forms.CharField(required=False, label='')
    category = forms.ChoiceField(choices=[('', 'Categories (All)')] + RecycleItem.CATEGORY_CHOICES, required=False, label='')
    condition = forms.ChoiceField(choices=[('', 'Condition (All)')] + RecycleItem.CONDITION_CHOICES, required=False, label='')
    location = forms.CharField(required=False, label='')
    sort_by = forms.ChoiceField(
        choices=[
            ('-created_at', 'Most Recent'),
            ('created_at', 'Least Recent'),
            ('-condition', 'Condition'),
        ],
        required=False,
        label=''
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keyword'].widget.attrs.update({'placeholder': 'Enter search keyword'})
        self.fields['category'].widget.attrs.update({'placeholder': 'Category'})
        self.fields['condition'].widget.attrs.update({'placeholder': 'Condition'})
        self.fields['location'].widget.attrs.update({'placeholder': 'Location (postal code, city, province, country...)'})
        self.fields['sort_by'].widget.attrs.update({'placeholder': 'Sort By'})

        self.helper = FormHelper()
        self.helper.add_input(Submit('search', 'Search'))


class EditRecycleItemForm(forms.ModelForm):
    class Meta:
        model = RecycleItem
        fields = ['item_type', 'description', 'condition', 'category', 'email', 'phone_number', 'address', 'city', 'province',
                  'postal_code', 'country', 'image']

    def __init__(self, *args, **kwargs):
        super(EditRecycleItemForm, self).__init__(*args, **kwargs)

        # List of fields to be made required
        required_fields = ['email', 'phone_number', 'address', 'city', 'province', 'postal_code', 'country']

        for field in required_fields:
            self.fields[field].required = True


class HomepageSearchForm(forms.Form):
    keyword = forms.CharField(required=False, label='')
    category = forms.ChoiceField(choices=[('', 'Categories (All)')] + RecycleItem.CATEGORY_CHOICES, required=False,
                                 label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keyword'].widget.attrs.update({
            'placeholder': 'Enter search keyword',
            'class': 'search-home-input'
        })
        self.fields['category'].widget.attrs.update({
            'placeholder': 'Category',
            'class': 'search-home-input'
        })

        self.helper = FormHelper()
        self.helper.add_input(Submit('search', 'Search'))
