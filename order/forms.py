from django import forms
from .models import Order


class SearchOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_id',)


class RawSearchOrder(forms.Form):
    order_id = forms.CharField(
        label='',
        initial="order#",
        widget=forms.TextInput(
            attrs={"class": "form-control mr-sm-2", "placeholder": "Search order"})
    )
