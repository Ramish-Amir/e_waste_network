# middlewares.py

import datetime
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from datetime import date

class TrackVisitDurationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.get('visit_start'):
            request.session['visit_start'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not request.session.get('actions_taken_today'):
            request.session['actions_taken_today'] = 0
        return None

    def process_response(self, request, response):
        visit_start_str = request.session.get('visit_start')
        if visit_start_str:
            try:
                visit_start = datetime.datetime.strptime(visit_start_str, '%Y-%m-%d %H:%M:%S')
                visit_duration = (datetime.datetime.now() - visit_start).total_seconds()
                if 'total_visit_duration_today' in request.session:
                    request.session['total_visit_duration_today'] += visit_duration
                else:
                    request.session['total_visit_duration_today'] = visit_duration
            except (ValueError, TypeError):
                request.session['visit_start'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['visit_start'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return response


class TrackUserLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            today = date.today().strftime("%Y-%m-%d")
            session_key = f"visits_{today}"

            if session_key not in request.session:
                request.session[session_key] = 0

            request.session[session_key] += 1

        return response