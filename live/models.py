import random
from django.db import models


class Event(models.Model):

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    title = models.CharField(max_length=40)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s' % (self.title)


class MealEvent(models.Model):
    '''
    A meal event is a specific meal or snack time at the hackathon. This
    class allows for tracking of specific groups that summoned to eat at
    different times. This information can then be published to the
    top of the live listing on the website.
    '''
    title = models.CharField(max_length=40)
    #: Text to be displayed along with the event. Examples include
    #:  "coming soon" and "serving now"
    status = models.CharField(max_length=200, default='coming soon')
    
    #: Should this event be displayed in the events list?
    enabled = models.BooleanField(default=False)
    #: Should this event be pinned at the top of the events list?
    pin = models.BooleanField(default=True)

    # Groups
    now_serving = models.CharField(max_length=200)
    already_served = models.CharField(max_length=200)
    not_served = models.CharField(max_length=200)
