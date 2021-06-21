from datetime import datetime
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
import django

class QueueInfo(models.Model):
    class InactivityActions(models.TextChoices):
        DELETE = 'DL', _('Delete')
        MOVE_TO_END = 'ME', _('Move To End')

    service_id = models.CharField(max_length=32, default="")
    api_token = models.CharField(max_length=32, default="") # remove this
    queue_name = models.CharField(max_length=32, default="")
    max_users = models.IntegerField(default=0)
    now_serving = models.PositiveBigIntegerField(default=0)
    average_wait_time = models.FloatField(default=0.0)
    cohort_size = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    num_processed = models.IntegerField(default=0) # Number of users that have gone through the queue for average calculations.
    start_time = models.DateTimeField(default=django.utils.timezone.now)  # when queue is scheduled to open.
    stop_time = models.DateTimeField(default=datetime.max)  # when queue is schedule to close
    decommission_time = models.DateTimeField(default=datetime.max) # when table entry can be cleaned up.
    inactive_time = models.IntegerField(default=5)  # time in minutes before user is consider inactive.
    action_when_inactive = models.CharField(max_length=2, choices=InactivityActions.choices, default=InactivityActions.DELETE,) # JMR - Bool active/inactive
    rate = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "Queue Info Objects"

    def __str__(self):
        return self.queue_name


class QueuePosition(models.Model):
    queue_position = models.BigAutoField(primary_key=True, editable=False, )
    queue_info = models.ForeignKey(QueueInfo, on_delete=models.CASCADE, related_name='queue')

    def __str__(self):
        return self.queue_position


class UserInfo(models.Model):
    class UserTypes(models.TextChoices):
        PREMIUM = 'PR', _('Premium')
        REGULAR = 'RG', _('Regular')

    # queue_info = models.ForeignKey(QueueInfo, on_delete=models.CASCADE, related_name='queue')
    queue_index = models.BigAutoField(primary_key=True, editable=False,)
    queue_position = models.ForeignKey(QueuePosition, on_delete=models.CASCADE, related_name='position', null=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    time_entered = models.DateTimeField(default=django.utils.timezone.now)
    time_exited = models.DateTimeField(null=True)
    last_checkin = models.DateTimeField(default=django.utils.timezone.now)
    cohort = models.IntegerField(default=0)
    user_weight = models.CharField(max_length=2, choices=UserTypes.choices, default=UserTypes.REGULAR,)

    class Meta:
        verbose_name_plural = "User Info Objects"

