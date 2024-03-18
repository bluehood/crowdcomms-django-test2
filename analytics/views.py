from datetime import datetime

from django.utils import timezone
from .models import UserVisit

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloWorld(APIView):
    """
    Basic 'Hello World' view. Show our current API version, the current time, the number of recent visitors
    in the last 1 hour, and the total number of visitors and page visits
    """

    def get(self, request, format=None):
        # Get current time
        current_time = timezone.now()
        
        # Account for the request made to the /helloworld/ endpoint
        if request.user.is_authenticated and request.path == '/helloworld/':
            user_visit, created = UserVisit.objects.get_or_create(user=request.user)
            user_visit.last_seen = timezone.now()
            user_visit.visits += 1
            user_visit.save()

        # Filter for vistors that have visted the app in the last hour
        recent_visitors = UserVisit.objects.filter(last_seen__gte=current_time - timezone.timedelta(hours=1))
        num_recent_visitors = recent_visitors.count()

        # Get a list of all vistors and the count the number of vistors
        all_vistors = UserVisit.objects.values('user')
        num_all_vistors = 0
        for item in all_vistors:
            num_all_vistors += 1
        
        # Get total number of page vists per user
        all_visits = UserVisit.objects.values('visits')
        num_all_visits = 0
        for item in all_visits:
            num_all_visits += int(item['visits'])

        data = {
            'version': 1.0,
            'time': current_time,
            'recent_visitors': num_recent_visitors,
            'all_visitors': num_all_vistors,
            'all_visits': num_all_visits,
        }
        return Response(data)

