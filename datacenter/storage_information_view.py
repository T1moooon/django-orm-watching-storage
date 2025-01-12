from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Visit


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
 
    for visit in visits:
        enter_time = localtime(visit.entered_at)
        visit_duration = Visit.get_duration(visit)
        duration = Visit.format_duration(visit_duration)
        non_closed_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': enter_time,
            'duration': duration,
        })
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
