from django import forms
from .models import Item, Category


class NewProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                          "style": "text-align:center",
                                                          "placeholder": "Product name"}))

    category = forms.ModelChoiceField(Category.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))

    price = forms.FloatField(widget=forms.NumberInput(attrs={"class": "form-control",
                                                             "style": "text-align:center",
                                                             "placeholder": "Price"}))

    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",
                                                               "style": "text-align:center",
                                                               "placeholder": "Description",
                                                               "rows": 5}))

    quantity_on_stock = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control",
                                                                           "style": "text-align:center",
                                                                           "placeholder": "Quantity"}))

    class Meta:
        model = Item
        fields = ('title',
                  'category',
                  'price',
                  'description',
                  'quantity_on_stock',
                  )


class SearchForProduct(forms.ModelForm):
    title = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={"class": "form-control",
                                                          "style": "text-align:center",
                                                          "placeholder": "search by title"}))
    description = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={"class": "form-control",
                                                                "style": "text-align:center",
                                                                "placeholder": "search by description"}))

    class Meta:
        model = Item
        fields = ('title',
                  'description',
                  )


class NewCategoryForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                          "style": "text-align:center",
                                                          "placeholder": "Category name"}))

    class Meta:
        model = Category
        fields = ('title',
                  )


class SearchForCategory(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                          "style": "text-align:center",
                                                          "placeholder": "search category"}))

    class Meta:
        model = Category
        fields = ('title',
                  )
