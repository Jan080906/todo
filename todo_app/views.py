from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .models import Task
from .serializers import TaskSerializer, TaskCreateInputSerializer, TaskUpdateInputSerializer

@api_view(['GET','POST'])
def tasks(request):
    user = request.user

    # GET Tasks
    if request.method == 'GET':
        if user.is_staff == True:
            query_set = Task.objects.select_related('user').all()
        else:
            query_set = Task.objects.filter(user_id=user.id).select_related('user')
        serializer = TaskSerializer(query_set, many=True)
        return Response(serializer.data)

    # ADD Task
    elif request.method == 'POST':
        serializer = TaskCreateInputSerializer(data=request.data, context={'user_id': request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT', 'DELETE'])
def task(request, id):
    task = get_object_or_404(Task, pk=id)

    # Permission check
    if (request.user.id != task.user_id):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # GET Task
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    # UPDATE Task
    elif request.method == 'PUT':
        serializer = TaskUpdateInputSerializer(task, data=request.data, context={'user_id': request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_200_OK)

    # DELETE Task
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
