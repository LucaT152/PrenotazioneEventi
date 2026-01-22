import datetime
from django import forms
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter date.", input_formats=["%d-%m-%Y"], widget=forms.TextInput(attrs={'placeholder':'gg-mm-aaaa'}))

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError('Invalid - renewal in past')
        if data > (datetime.date.today() +datetime.timedelta(weeks=4)):
            raise ValidationError('Invalid date - too late')
        return data
    


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username', 'password1', 'password2']
