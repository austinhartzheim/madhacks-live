from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.template import RequestContext

from vote.models import *
from vote.forms import *

from live.models import *

import datetime, gspread, dateutil.parser
import madhacks.settings


def main_live(request):
    '''
    Show the screen prompting the user to enter their email address
    before they go on with the voting.
    '''
    currdatetime = datetime.datetime.now()

    events = Event.objects.filter(start_date__lt=currdatetime + datetime.timedelta(hours=1)).filter(end_date__gt=currdatetime)
    mealevent = MealEvent.objects.all()[0]

    return render_to_response('live/main.html',
                              {'events': events,
                               'mealevent': mealevent,
                              'form': EntryForm},
                              RequestContext(request))


def fetch(request):
    '''
    Populates the DB with events from google spreadsheet
    '''
    # Login with your Google account
    gc = gspread.login(madhacks.settings.DRIVE_LOGIN, madhacks.settings.DRIVE_PASS)

    # Open a worksheet from spreadsheet with one shot
    wks = gc.open_by_key("1CoJb3Ondc0OS7dOOp7DQkywdS7W7d96D4QodkwCCghg").sheet1

    #snag columns from spreadsheet
    dates = wks.col_values(1)[1:] # slice away the first row that has the col name
    start_times = wks.col_values(2)[1:]
    end_times = wks.col_values(3)[1:]
    event_names = wks.col_values(5)[1:]

    # loop through events, add them as models in the DB
    for i in range(len(event_names)):
        if event_names[i]:
            print dates[i], " ", start_times[i], " ", end_times[i], " ", event_names[i]
            print "Starting at: ", dateutil.parser.parse(dates[i]+ " "+ start_times[i])
            print "Ending at: ", dateutil.parser.parse(dates[i]+ " "+ end_times[i])
            e = Event(start_date=dateutil.parser.parse(dates[i]+ " "+ start_times[i]),
                      end_date = dateutil.parser.parse(dates[i]+ " "+ end_times[i]),
                      title=event_names[i],
                      description="")

            e.save()




    currdatetime = datetime.datetime.now()

    events = Event.objects.filter(start_date__lt=currdatetime + datetime.timedelta(hours=1)).filter(end_date__gt=currdatetime)
    mealevents = MealEvent.objects.filter()

    return render_to_response('live/fetch.html',
                              {'events': events,
                               'mealevents': mealevents,
                              'form': EntryForm},
                              RequestContext(request))



