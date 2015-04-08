import random
from django.db import models


class Event(models.Model):
    # TODO: decide on how time-zones will be handled and where they will
    #   be handled.
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    title = models.CharField(max_length=40)
    description = models.TextField()


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

    def get_groups_now_serving(self):
        return self.now_serving.split(', ')

    def get_groups_already_served(self):
        return self.already_served.split(', ')

    def get_groups_not_served(self):
        return self.not_served.split(', ')

    def add_group_not_served(self, groupname):
        groupname = groupname.replace(',', '')
        groups = self.not_served.split(', ')
        if groupname not in groups:
            self.not_served += ', ' + groupname

    def serve_random_groups(self, n=1):
        '''
        Selects n random groups from the not_serving list and moves them
        to the front of the now_serving list (allowing this list to act
        as a sort of queue).
        '''
        not_serving = self.not_served.split(', ')
        now_serving = self.now_serving

        while n > 0:
            e = not_serving.pop(random.randint(0, len(not_serving)-1))
            now_serving = e + ', ' + now_serving
            n -= 1

        self.now_serving = now_serving
        self.not_serving = ', '.join(not_serving)

    def served_groups(self, n=1):
        '''
        Selects the last n groups from the now_serving list and moves
        them to the already_served list (which is re-sorted).
        '''
        now_serving = self.now_serving.split(', ')
        already_served = self.already_served.split(', ')

        while n > 0 and now_serving:
            e = now_serving.pop()
            already_served.append(e)
        already_served.sort()

        self.now_serving = ', '.join(now_serving)
        self.already_served = ', '.join(already_served)
