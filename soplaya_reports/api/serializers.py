from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Serializer per i report."""

    total_planned_hours = serializers.IntegerField(read_only=True)
    total_actual_hours = serializers.IntegerField(read_only=True)
    total_budget = serializers.DecimalField(max_digits=10, decimal_places=2,
                                            read_only=True)
    total_sells = serializers.DecimalField(max_digits=10, decimal_places=2,
                                           read_only=True)
    total_hours_difference = serializers.IntegerField(read_only=True)
    total_budget_difference = serializers.DecimalField(max_digits=10, decimal_places=2,
                                                       read_only=True)

    class Meta:
        model = Report
        fields = ['date', 'restaurant', 'total_planned_hours', 'total_actual_hours',
                  'total_budget', 'total_sells', 'total_hours_difference',
                  'total_budget_difference']
