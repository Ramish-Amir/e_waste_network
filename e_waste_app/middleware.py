# middlewares.py

import datetime
from django.utils.deprecation import MiddlewareMixin

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
