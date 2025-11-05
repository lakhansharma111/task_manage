from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from datetime import datetime


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD for tasks with filtering and complete/incomplete actions."""
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed', 'priority']

    def list(self, request, *args, **kwargs):
        """Supports query params: completed (true/false), priority, due_before, due_after, limit, offset"""
        qs = self.get_queryset()
        completed_q = request.query_params.get('completed')
        if completed_q is not None:
            completed_q = completed_q.lower()
            if completed_q in ('true', '1'):
                qs = qs.filter(completed=True)
            elif completed_q in ('false', '0'):
                qs = qs.filter(completed=False)
        priority = request.query_params.get('priority')
        if priority:
            qs = qs.filter(priority=priority)
        due_before = request.query_params.get('due_before')
        if due_before:
            try:
                db = datetime.strptime(due_before, '%Y-%m-%d').date()
                qs = qs.filter(due_date__lte=db)
            except ValueError:
                return Response({'detail': 'due_before must be YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        due_after = request.query_params.get('due_after')
        if due_after:
            try:
                da = datetime.strptime(due_after, '%Y-%m-%d').date()
                qs = qs.filter(due_date__gte=da)
            except ValueError:
                return Response({'detail': 'due_after must be YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        # simple pagination
        try:
            limit = int(request.query_params.get('limit', 100))
            offset = int(request.query_params.get('offset', 0))
        except ValueError:
            return Response({'detail': 'limit and offset must be integers'}, status=status.HTTP_400_BAD_REQUEST)
        qs = qs[offset:offset + limit]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        if task.completed:
            return Response({'detail': 'Task already completed'}, status=status.HTTP_400_BAD_REQUEST)
        task.completed = True
        task.save()
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=['post'])
    def incomplete(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        if not task.completed:
            return Response({'detail': 'Task already incomplete'}, status=status.HTTP_400_BAD_REQUEST)
        task.completed = False
        task.save()
        return Response(self.get_serializer(task).data)