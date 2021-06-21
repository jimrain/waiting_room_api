import datetime
import http

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from waiting_room_api.models import QueueInfo, UserInfo
from waiting_room_api.serializers import QueueInfoSerializer, UserInfoSerializer, QueuePositionSerializer

@csrf_exempt
def queue_info_list(request):
    """
    List all code queue_info, or create a new queue_info.
    """
    if request.method == 'GET':
        snippets = QueueInfo.objects.all()
        serializer = QueueInfoSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = QueueInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def queue_info_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        qi = QueueInfo.objects.get(pk=pk)
    except QueueInfo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = QueueInfoSerializer(qi)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = QueueInfoSerializer(qi, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        qi.delete()
        return HttpResponse(status=204)

@csrf_exempt
def user_info_list(request):
    """
    List all code queue_info, or create a new queue_info.
    """
    if request.method == 'GET':
        ui = UserInfo.objects.all()
        serializer = UserInfoSerializer(ui, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        print(request.body)
        data = JSONParser().parse(request)
        try:
            q_name = data.pop('queue_name')
            qi = QueueInfo.objects.get(queue_name=q_name)
            data.update({"queue_info": qi.id})
        except (KeyError, QueueInfo.DoesNotExist):
            # Either the q name was not in the post info or the queue was not found in the database.
            return HttpResponse(status=404)

        serializer = UserInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_queue_position(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            q_name = data.pop('queue_name')
            qi = QueueInfo.objects.get(queue_name=q_name)
            data.update({"queue_info": qi.id})
        except (KeyError, QueueInfo.DoesNotExist):
            # Either the q name was not in the post info or the queue was not found in the database.
            return HttpResponse(status=404)

        # print(data)
        serializer = QueuePositionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_queue_release(request, pk):
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        time_in_queue = data.pop('time_in_queue')
        try:
            qi = QueueInfo.objects.get(pk=pk)
        except (KeyError, QueueInfo.DoesNotExist):
            # the queue was not found in the database.
            return HttpResponse(status=404)

        qi.num_processed = qi.num_processed + 1

        serializer = QueueInfoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_info_checkin(request, pk):
    try:
        ui = UserInfo.objects.get(pk=pk)
    except UserInfo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':

        serializer = UserInfoSerializer(ui, data={"last_checkin": datetime.datetime.now()}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # This should always be a PUT
    return JsonResponse(http.HTTPStatus.METHOD_NOT_ALLOWED, status=400)