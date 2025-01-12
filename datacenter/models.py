from django.db import models
from django.utils.timezone import localtime


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
        current_time = localtime()
        enter_time = localtime(self.entered_at)
        duration = current_time - enter_time
        return int(duration.total_seconds())

    def format_duration(self):
        hours, remainder = divmod(self, 3600)
        minutes, _ = divmod(remainder, 60)
        return f'{hours}ч {minutes}мин'

    def is_visit_long(self, check_minutes=60):
        if self.leaved_at is None:
            return "Еще внутри"
        entered_time = localtime(self.entered_at)
        leaved_time = localtime(self.leaved_at)
        delta = leaved_time - entered_time
        delta_seconds = delta.total_seconds()
        duration_in_minutes = delta_seconds // 60
        return duration_in_minutes >= check_minutes
