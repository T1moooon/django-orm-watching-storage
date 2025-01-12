from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits_passcard = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []

    for visit in visits_passcard:
        delta = visit.leaved_at - visit.entered_at
        duration_seconds = delta.total_seconds()
        is_strange = Visit.is_visit_long(visit, 60)
        this_passcard_visits.append({
            'entered_at': visit.entered_at,
            'duration': Visit.format_duration(duration_seconds),
            'is_strange': is_strange,
        })
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
