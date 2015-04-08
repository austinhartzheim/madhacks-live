from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.template import RequestContext

from vote.models import *
from vote.forms import *

ERRORTEXT_EMAIL_NOT_REGISTERED = ('That email is not registered. Make sure '
                                  'to use the same email that you entered '
                                  'when you RSVPed to MadHacks.')
ERRORTEXT_INVALID_EMAIL = ('The email address you entered is invalid.')
ERRORTEXT_ACCESS_DENIED = ('You do not have permission to vote. You might '
                           'have already voted or you might be expected to '
                           'vote through another system. Please check with '
                           'an event staff if you have questions.')
ERRORTEXT_ALREADY_VOTED = ('You have already voted.')

def vote_enter_prompt(request):
    '''
    Show the screen prompting the user to enter their email address
    before they go on with the voting.
    '''
    return render_to_response('vote/enter_prompt.tpl.html',
                              {'form': EntryForm},
                              RequestContext(request))


def vote_enter_submit(request):
    '''
    The user has given us their unique identifier. Confirm that they
    have not already voted. If they have voted, redirect them to an
    error screen. If they have not, generate a unique voting page for
    them containing the necessary information to record their vote.
    '''
    form = EntryForm(request.POST)

    # Check that the email is included
    if not form.is_valid():
        return render_to_response('vote/enter_prompt.tpl.html',
                                  {'form': form},
                                  RequestContext(request))

    # Check if the email is associated with a registered user
    email = form.cleaned_data['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return render_to_response('vote/enter_prompt.tpl.html',
                                  {'form': form,
                                   'error': ERRORTEXT_EMAIL_NOT_REGISTERED},
                                  RequestContext(request))
    
    # Check the status table to see if the user has not voted.
    try:
        status = Status.objects.get(user=user)
        if status.voted:
            return render_to_response('vote/enter_prompt_tpl.html',
                                      {'form': form,
                                       'error': ERRORTEXT_ALREADY_VOTED},
                                      RequestContext(request))
    except Status.DoesNotExist:
        return render_to_response('vote/enter_prompt.tpl.html',
                                  {'form': form,
                                   'error': ERRORTEXT_EMAIL_NOT_REGISTERED},
                                  RequestContext(request))

    # TODO: craft the page where the user can submit votes. This
    #   means we should use a Django form.
    '''
    polls = Poll.objects.filter(active=True)
    VoteFormFormSet = formset_factory(VoteForm, extra=len(polls)-1)
    formset = VoteFormFormSet(initial=list(
            {'poll_pk': poll.pk,
             'poll_title': poll.name} for poll in polls))

    print(formset)

    return render_to_response('vote/vote_page.tpl.html',
                              {'email': request.POST['email'],
                               'formset': formset},
                              RequestContext(request))
    '''

    polls = Poll.objects.filter(active=True)
    forms = list(
        {'title': poll.name, 'pk': poll.pk, 'form': VoteForm(prefix=poll.pk),
         'description': poll.description} for poll in polls
    )

    return render_to_response('vote/vote_page.tpl.html',
                              {'email': request.POST['email'],
                               'forms': forms},
                              RequestContext(request))

def vote_submit(request):
    '''
    Record the vote, mark the User object associated with the unique
    identifier as having voted, and redirect the user to a page that
    thanks them for their vote.
    '''
    # TODO: check again that the user is allowed to vote (they are
    #   registered and are still a member of the group allowed to vote)
    # TODO: check that the votes are valid. If they are not valid,
    #   render the vote_page.tpl.html page again with the form filled
    #   in and invalid entries highlighted.
    # TODO: populate vote objects and save them.
    # TODO: mark the user as having voted by removing from the group
    #   of people who need to vote.
    pass
