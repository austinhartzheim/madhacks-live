from django.core.management.base import BaseCommand, CommandError
from vote.models import *

NUM_TOP_TEAMS = 3

class Command(BaseCommand):
    help = 'Displays the current vote totals.'

    def handle(self, **options):
        for poll in Poll.objects.all():
            if poll.active:
                print(' - Poll: %s [active]' % poll.name)
            else:
                print(' - Poll: %s [inactive]' % poll.name)

            votes = Vote.objects.filter(poll=poll)
            voted_users = []
            teams = {}

            for vote in votes:
                if vote.user in voted_users:
                    # TODO: confirm that `ordering` from Vote's Meta class
                    #  is being applied to select the first vote only
                    continue  # Only count first vote
                voted_users.append(vote.user)
                if vote.place1 in teams:
                    teams[vote.place1] += 3
                elif vote.place1 != None:
                    teams[vote.place1] = 3

                if vote.place2 in teams:
                    teams[vote.place2] += 2
                elif vote.place2 != None:
                    teams[vote.place2] = 2

                if vote.place3 in teams:
                    teams[vote.place3] += 1
                elif vote.place3 != None:
                    teams[vote.place3] = 1

            # Rank the teams
            thresholds = [0] * NUM_TOP_TEAMS
            top_teams = [None] * NUM_TOP_TEAMS

            for team in teams:
                for i in range(0, NUM_TOP_TEAMS):
                    if teams[team] > thresholds[i]:
                        thresholds.insert(i, teams[team])
                        thresholds.pop()
                        top_teams.insert(i, team)
                        top_teams.pop()
                        break

            for i in range(0, NUM_TOP_TEAMS):
                print('  {0:30} {1}'.format(top_teams[i], thresholds[i]))
