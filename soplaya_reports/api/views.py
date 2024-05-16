from django.db.models import Sum, F
from rest_framework import viewsets, filters, pagination, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Report
from .serializers import ReportSerializer


class CustomPagination(pagination.PageNumberPagination):
    """Paginazione personalizzata per i report."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportViewSet(viewsets.ModelViewSet):
    """ViewSet per i report."""

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,
                       DjangoFilterBackend]
    filterset_fields = ['restaurant', 'date']
    ordering_fields = ['date', 'restaurant', 'total_planned_hours',
                       'total_actual_hours', 'total_budget', 'total_sells',
                       'total_hours_difference', 'total_budget_difference']
    pagination_class = CustomPagination

    def get_queryset(self):
        """Restituisce i report filtrati."""

        queryset = super().get_queryset()

        # Filtering by date range
        date_gte = self.request.query_params.get('date__gte')
        date_lte = self.request.query_params.get('date__lte')
        if date_gte:
            queryset = queryset.filter(date__gte=date_gte)
        if date_lte:
            queryset = queryset.filter(date__lte=date_lte)

        # Grouping data by date and restaurant with SUM aggregation
        queryset = queryset.values('date', 'restaurant').annotate(
            total_planned_hours=Sum('planned_hours'),
            total_actual_hours=Sum('actual_hours'),
            total_budget=Sum('budget'),
            total_sells=Sum('sells')
        )

        # Calculating additional fields
        for item in queryset:
            item['total_hours_difference'] = item['total_planned_hours'] - item[
                'total_actual_hours']
            item['total_budget_difference'] = item['total_budget'] - item['total_sells']

        return queryset

