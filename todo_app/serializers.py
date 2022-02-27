from rest_framework import serializers
from todo_app.models import Task
from django.contrib.auth.models import User
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']
    name = serializers.CharField(max_length=150, source='username')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description','sequence', 'user', 'last_updated']
    user = UserSerializer()

class TaskCreateInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description','sequence']

    def create(self, validated_data):
        task = Task(**validated_data)
        task.user_id = 1
        task.last_updated = datetime.utcnow()
        task.save()
        return task

class TaskUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=255, required=False)
    sequence = serializers.IntegerField(required=False)
    status = serializers.CharField(max_length=10, required=False)

    def update(self, instance, validated_data):
        title = validated_data.get('title',None)
        description = validated_data.get('description',None)
        sequence = validated_data.get('sequence',None)
        status = validated_data.get('status',None)
        if title is not None:
            instance.title = validated_data['title']
        if description is not None:
            instance.description = validated_data['description']
        if sequence is not None:
            instance.sequence = validated_data['sequence']
        if status is not None:
            instance.status = validated_data['status']
        instance.save()
        return instance
