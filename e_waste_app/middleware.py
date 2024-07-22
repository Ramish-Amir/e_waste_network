from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from .models import UserVisit

class TrackUserVisitsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # Start a new visit
            request.session['visit_start'] = datetime.now().isoformat()

    def process_response(self, request, response):
        if request.user.is_authenticated:
            visit_start = request.session.get('visit_start')
            if visit_start:
                visit_start = datetime.fromisoformat(visit_start)
                visit_end = datetime.now()

                # Save visit duration
                UserVisit.objects.create(
                    user=request.user,
                    visit_start=visit_start,
                    visit_end=visit_end
                )
        return response
