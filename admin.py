from django.contrib import admin
from waiting_room_api.models import QueueInfo, UserInfo, QueuePosition

admin.site.register(QueueInfo)
admin.site.register(UserInfo)
admin.site.register(QueuePosition)
