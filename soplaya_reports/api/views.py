from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['restaurant', 'date']
    ordering_fields = ['date', 'planned_hours', 'actual_hours', 'budget', 'sells']
