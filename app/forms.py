from django import forms


class SearchForm(forms.Form):
    key_word = forms.CharField(label='キーワード', required=False)
