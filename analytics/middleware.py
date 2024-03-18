from django.utils import timezone
from .models import UserVisit

class UserVisitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If a user is authenticated capture analytics data 
        if request.user.is_authenticated:
            user_visit, created = UserVisit.objects.get_or_create(user=request.user)
            user_visit.last_seen = timezone.now()
            user_visit.visits += 1
            user_visit.save()

        return response
