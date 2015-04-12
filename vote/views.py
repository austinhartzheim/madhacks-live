from django.http import HttpResponseRedirect
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
ERRORTEXT_COOKIES_ENABLED = ('You must have cookies enabled to use this form. '
                             'Please check that they are enabled.')
ERRORTEXT_INVALID_TEAM_CHOICE = ('You have selected an invalid team. '
                                 'Please try voting again. If this error'
                                 'persists, please contact an administrator.')

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
        request.session['upk'] = user.pk
    except User.DoesNotExist:
        return render_to_response('vote/enter_prompt.tpl.html',
                                  {'form': form,
                                   'error': ERRORTEXT_EMAIL_NOT_REGISTERED},
                                  RequestContext(request))
    
    # Check the status table to see if the user has not voted.
    try:
        status = Status.objects.get(user=user)
        if status.voted:
            return render_to_response('vote/enter_prompt.tpl.html',
                                      {'form': form,
                                       'error': ERRORTEXT_ALREADY_VOTED},
                                      RequestContext(request))
    except Status.DoesNotExist:
        return render_to_response('vote/enter_prompt.tpl.html',
                                  {'form': form,
                                   'error': ERRORTEXT_EMAIL_NOT_REGISTERED},
                                  RequestContext(request))

    polls = Poll.objects.filter(active=True)
    forms = list(
        {'title': poll.name, 'pk': poll.pk, 'form': VoteForm(prefix=poll.pk),
         'description': poll.description} for poll in polls
    )

    return render_to_response('vote/vote_page.tpl.html',
                              {'forms': forms},
                              RequestContext(request))

def vote_submit(request):
    '''
    Record the vote, mark the User object associated with the unique
    identifier as having voted, and redirect the user to a page that
    thanks them for their vote.
    '''
    # Fetch the user ID from request.session
    upk = request.session.get('upk', None)
    if upk == None:
        return render_to_response('vote/error.tpl.html',
                                  {'error': ERRORTEXT_COOKIES_ENABLED},
                                  RequestContext(request))
    user = User.objects.get(pk=upk)

    # Check the status table to see if the user has voted
    try:
        status = Status.objects.get(user=user)
        if status.voted:
            return render_to_response('vote/error_prompt.tpl.html',
                                      {'error': ERRORTEXT_ALREADY_VOTED},
                                      RequestContext(request))
    except Status.DoesNotExist:
        return render_to_response('vote/error.tpl.html',
                                  {'error': ERRORTEXT_EMAIL_NOT_REGISTERED},
                                  RequestContext(request))

    # Load and validate the form data
    vote_objects = []

    voteforms = []
    voteforms_are_valid = True
    polls = Poll.objects.filter(active=True)

    for poll in polls:
        voteform = VoteForm(request.POST, prefix=poll.pk)  # Unwrap factory
        if not voteform.is_valid():
            votesforms_are_valid = False
 
        voteobject = Vote()
        voteobject.user = user
        voteobject.poll = poll

        try:
            print(voteform.cleaned_data)
            votes = voteform.get_votes()
            voteobject.place1 = votes[0]
            voteobject.place2 = votes[1]
            voteobject.place3 = votes[2]
        except KeyError:
            polls = Poll.objects.filter(active=True)
            forms = list(
                {'title': poll.name, 'pk': poll.pk,
                 'form': VoteForm(prefix=poll.pk),
                 'description': poll.description} for poll in polls
            )

            return render_to_response('vote/vote_page.tpl.html',
                                      {'error': ERRORTEXT_INVALID_TEAM_CHOICE,
                                       'forms': forms},
                                      RequestContext(request))
        vote_objects.append(voteobject)

    # Check again if the user has voted (to prevent race conditions)
    try:
        status = Status.objects.get(user=user)
        if status.voted:
            return render_to_response('vote/error_prompt.tpl.html',
                                      {'error': ERRORTEXT_ALREADY_VOTED},
                                      RequestContext(request))
    except Status.DoesNotExist:
        return render_to_response('vote/error.tpl.html',
                                  {'error': ERRORTEXT_EMAIL_NOT_REGISTERED},
                                  RequestContext(request))
    
    # Mark the user as having voted
    status.voted = True
    status.save()

    # Save the vote objects
    for voteobject in vote_objects:
        voteobject.save()
    
    return HttpResponseRedirect('/vote/thanks')

def vote_thanks(request):
    '''
    Thank the user for their vote.
    '''
    return render_to_response('vote/thanks.tpl.html',
                              RequestContext(request))


def vote_error(request):
    '''
    Return a generic error page. (Although, a more specific error
    message would be better.)
    '''
    return render_to_response('vote/error.tpl.html',
                              RequestContext(request))
