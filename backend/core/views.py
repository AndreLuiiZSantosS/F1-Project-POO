from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Driver, Event


def _serialize_driver(driver):
    return {
        "id": driver.id,
        "name": driver.name,
        "number": driver.number,
        "team": driver.team.name,
        "active": driver.active,
    }


def _serialize_result(result):
    return {
        "id": result.id,
        "driver": _serialize_driver(result.driver),
        "position": result.position,
        "time": result.time,
        "status": result.status,
        "points": result.points,
    }


def _serialize_session(session):
    results = list(session.results.select_related("driver__team").all())
    return {
        "id": session.id,
        "name": session.name,
        "session_type": session.session_type,
        "session_number": session.session_number,
        "results": [_serialize_result(result) for result in results],
    }


def _serialize_event(event):
    sessions = list(event.sessions.all())
    return {
        "id": event.id,
        "name": event.name,
        "round_number": event.round_number,
        "circuit": event.circuit,
        "date": event.date.isoformat() if event.date else None,
        "has_sprint": event.has_sprint,
        "practice_sessions_count": event.practice_sessions_count,
        "qualifying_sessions_count": event.qualifying_sessions_count,
        "drivers": [_serialize_driver(driver) for driver in Driver.objects.filter(active=True).select_related("team")],
        "sessions": [_serialize_session(session) for session in sessions],
    }


@csrf_exempt
def events_view(request):
    if request.method != "GET":
        return JsonResponse({"error": "Metodo nao permitido"}, status=405)

    events = Event.objects.prefetch_related("sessions__results__driver__team").order_by("round_number")
    return JsonResponse({"events": [_serialize_event(event) for event in events]})
