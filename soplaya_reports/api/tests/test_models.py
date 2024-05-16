from django.test import TestCase
from api.models import Report


class ReportModelTestCase(TestCase):
    def setUp(self):
        self.report = Report.objects.create(
            date='2024-05-16',
            restaurant='Test Restaurant',
            planned_hours=8,
            actual_hours=7,
            budget=1000.00,
            sells=900.00
        )

    def test_hours_difference(self):
        self.assertEqual(self.report.hours_difference, 1)

    def test_budget_difference(self):
        self.assertEqual(self.report.budget_difference, 100.00)
