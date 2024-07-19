from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.core.exceptions import ValidationError

from .models import ContactMessage
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",
                                                             'id': 'inputUsername3',
                                                             'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput({'class': 'form-control',
                                                           'id': 'inputPassword3',
                                                           'placeholder': 'password'}))


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords must match')
        return cleaned_data

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = User.objects.create_user(username=username, email=email, password=password)
        return user


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Enter your email address')


class PasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        # Extract user if present
        user = kwargs.pop('user', None)
        super().__init__(user=user, *args, **kwargs)
        #super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm new password'})

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            self._validate_password(password)
        return password

    def _validate_password(self, password):
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')

        if password.isdigit():
            raise ValidationError('Password must not contain only numbers')

        common_passwords = ['qwerty@123', '12345678']
        if password in common_passwords:
            raise ValidationError('Password can’t be a commonly used password')

        '''validators = [CommonPasswordValidator()]
        for validator in validators:
            try:
                validator.validate(password)
            except ValidationError as e:
                raise ValidationError(e.message)'''