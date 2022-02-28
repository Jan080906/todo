from rest_framework import serializers
from todo_app.models import Task
from django.contrib.auth.models import User
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']
    name = serializers.CharField(max_length=150, source='first_name')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description','sequence', 'user', 'last_updated', 'status']
    user = UserSerializer()

class TaskCreateInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description']

    def create(self, validated_data):
        task = Task(**validated_data)
        task.user_id = self.context['user_id']
        task.last_updated = datetime.utcnow()
        tasks = Task.objects.filter(user_id=self.context['user_id'])
        if tasks:
            highest_sequence = max(task.sequence for task in tasks)
            task.sequence = highest_sequence + 1
        else:
            task.sequence = 1
        task.save()
        return task

class TaskUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=255, required=False)
    sequence = serializers.IntegerField(required=False)
    status = serializers.CharField(max_length=10, required=False)

    def validate(self, data):
        new_sequence = data.get('sequence',None)
        if new_sequence is not None:
            task = Task.objects.filter(user_id=self.context['user_id']).filter(sequence = new_sequence).first()
            if task is None:
                raise serializers.ValidationError(f'The provided sequence {new_sequence} is invalid')
        return data

    def update(self, instance, validated_data):
        new_title = validated_data.get('title',None)
        new_description = validated_data.get('description',None)
        new_sequence = validated_data.get('sequence',None)
        new_status = validated_data.get('status',None)
        if new_title is not None:
            instance.title = new_title
        if new_description is not None:
            instance.description = new_description
        if new_sequence is not None:
            # Reorder sequence
            self.reorder_sequence(instance.sequence,new_sequence, self.context['user_id'])
            instance.sequence = new_sequence
        if new_status is not None:
            instance.status = new_status
        instance.save() 
        return instance

    def reorder_sequence(self, current_sequence ,new_sequence , user_id):
        task = Task.objects.filter(user_id=user_id).filter(sequence = new_sequence).first()
        if task is not None:
            task.sequence = current_sequence
            task.save()

