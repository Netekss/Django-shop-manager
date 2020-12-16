from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as DjangoUser
from django import forms

from .models import User


class CreateUserForm(UserCreationForm):

    # user_type = forms.ModelChoiceField(UserType.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    user_type2 = forms.ChoiceField(choices=User.USER_TYPES, widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = DjangoUser
        fields = [
            'username',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'aria-describedby': 'inputGroup-sizing-default',
            'placeholder': 'username'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'aria-describedby': 'inputGroup-sizing-default',
            'placeholder': 'password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'aria-describedby': 'inputGroup-sizing-default',
            'placeholder': 'confirm password'
        })
