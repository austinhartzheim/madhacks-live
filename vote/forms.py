from django import forms
from django.forms.formsets import formset_factory
from vote.models import Team


class EntryForm(forms.Form):
    email = forms.EmailField(required=True)


class VoteForm(forms.Form):
    '''
    Collect actual votes from the user.
    '''
    first_place = forms.ModelChoiceField(Team.objects.all(), required=False,
                                         empty_label='Choose...')
    second_place = forms.ModelChoiceField(Team.objects.all(), required=False,
                                          empty_label='Choose...')
    third_place = forms.ModelChoiceField(Team.objects.all(), required=False,
                                         empty_label='Choose...')

    def get_votes(self):
        '''
        Return a list of the votes from first to third place.
        :raises KeyError: when one of the model choices does not
          actually exist (such as, when the user tampers with a the
          value field of a widget.
        '''
        self.is_valid()  # Needed to create self.cleaned_data
        data = self.cleaned_data
        ret = []

        ret.append(data['first_place'])
        if data['second_place'] != data['first_place']:
            ret.append(data['second_place'])
        else:
            ret.append(None)

        if ((data['third_place'] != data['first_place']) and
            (data['third_place'] != data['second_place'])):
            ret.append(data['third_place'])
        else:
            ret.append(None)

        return ret
