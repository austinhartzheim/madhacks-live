from django import forms
from django.forms.formsets import formset_factory


class EntryForm(forms.Form):
    email = forms.EmailField(required=True)


class VoteForm(forms.Form):
    '''
    Collect actual votes from the user.
    '''
    first_place = forms.CharField(max_length=8)
    second_place = forms.CharField(max_length=8)
    third_place = forms.CharField(max_length=8)
