from django.db import models
from django.utils.timezone import localtime


SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 3600


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        end_time = localtime(self.leaved_at) if self.leaved_at else localtime()
        entered_at_local = localtime(self.entered_at)
        duration = end_time - entered_at_local
        duration_in_seconds = int(duration.total_seconds())
        return duration_in_seconds

    def format_duration(self, duration_seconds):
        hours, remainder = divmod(duration_seconds, SECONDS_IN_HOUR)
        minutes, _ = divmod(remainder, SECONDS_IN_MINUTE)
        format_time = f'{int(hours)}ч {int(minutes)}мин'
        return format_time

    def is_visit_long(self, check_minutes=60):
        duration_seconds = self.get_duration()
        duration_in_minutes = duration_seconds // SECONDS_IN_MINUTE
        return duration_in_minutes >= check_minutes
