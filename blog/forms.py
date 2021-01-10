# Create a form for stock portfolio

# import forms system for django
from django import forms
from .models import Stock, Currency

# create class for stock form


class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ["ticker"]  # python list


class CurrencyForm(forms.ModelForm):
	class Meta:
		model = Currency
		fields = ["currencytype"]  # python list
