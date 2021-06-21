from rest_framework import serializers
from waiting_room_api.models import QueueInfo, UserInfo, QueuePosition

class QueueInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueInfo
        fields = ['service_id', 'api_token', 'queue_name', 'max_users', 'now_serving', 'num_processed', 'average_wait_time', 'cohort_size',
                  'active', 'start_time', 'stop_time', 'decommission_time', 'inactive_time', 'action_when_inactive',
                  'rate']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['queue_info', 'queue_index', 'uuid', 'time_entered', 'time_exited', 'last_checkin', 'cohort',
                  'user_weight']

class QueuePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueuePosition
        fields = ['queue_position', 'queue_info']