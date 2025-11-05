from rest_framework import serializers
from .models import Task
from datetime import date




class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Title cannot be empty')
        return value.strip()


    def validate_due_date(self, value):
        if value is not None and value < date.today():
            raise serializers.ValidationError('Due date cannot be in the past')
        return value


    def validate_priority(self, value):
        choices = {c[0] for c in Task.PRIORITY_CHOICES}
        if value not in choices:
            raise serializers.ValidationError(f'Priority must be one of: {choices}')
        return value