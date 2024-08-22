from django import forms
from .models import Category, Brand, Color

class AdvancedSearchForm(forms.Form):
    min_price = forms.IntegerField(
        required=False,
        label='Минимальная цена',
        widget=forms.NumberInput(attrs={'placeholder': 'От'})
    )
    max_price = forms.IntegerField(
        required=False,
        label='Максимальная цена',
        widget=forms.NumberInput(attrs={'placeholder': 'До'})
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Категория',
        widget=forms.CheckboxSelectMultiple
    )
    brand = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        label='Бренд',
        widget=forms.CheckboxSelectMultiple
    )
    color = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        required=False,
        label='Цвет',
        widget=forms.CheckboxSelectMultiple
    )
    product_name = forms.CharField(
        required=False,
        label='Название продукта',
        widget=forms.TextInput(attrs={'placeholder': 'Название продукта'})
    )

class SearchForm(forms.Form):
    product_name = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Искать товары', 'class': 'search-input'}))