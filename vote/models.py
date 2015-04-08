from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=64)
    identifier = models.CharField(max_length=8)

    project_name = models.CharField(max_length=64)
    project_description = models.TextField()

    # TODO: possibly add a space for team members if we are not storing
    #   this informaiton elsewhere.

    def __str__(self):
        return '%i: %s: %s' % (self.pk, self.name, self.project_name)


class Status(models.Model):
    user = models.ForeignKey(User)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return '%s: %s' % (self.user.email, self.voted)


class Vote(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
    
    place1 = models.ForeignKey(Team, blank=True,
                               related_name="%(app_label)s_%(class)s_related1")
    place2 = models.ForeignKey(Team, blank=True,
                               related_name="%(app_label)s_%(class)s_related2")
    place3 = models.ForeignKey(Team, blank=True,
                               related_name="%(app_label)s_%(class)s_related3")

    def __str__(self):
        return '%s: %s: %i, %i, %i' % (self.poll, self.user.email, self.place1,
                                       self.place2, self.place3)

    class Meta:
        '''
        Permissions:
          view_totals: this is intended for event administrators/staff
            that should be allowed to compute the vote totals.
          submit_vote: this is indended for the normal event audience
            that will be submitting a vote. This permission should be
            removed after they have voted to prevent re-voting.
        '''
        permissions = (
            ("view_totals", "Allowed to calculate the vote totals."),
            ("submit_vote", "Allowed to submit a vote"),
        )
