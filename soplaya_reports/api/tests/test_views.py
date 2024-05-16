from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Report
from api.views import ReportViewSet


class ReportAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Report.objects.create(
            date='2024-05-16',
            restaurant='Test Restaurant',
            planned_hours=8,
            actual_hours=7,
            budget=1000.00,
            sells=900.00
        )
        Report.objects.create(
            date='2024-05-16',
            restaurant='Test Restaurant',
            planned_hours=8,
            actual_hours=6,
            budget=1000.00,
            sells=900.00
        )
        Report.objects.create(
            date='2024-05-13',
            restaurant='Test Restaurant 2',
            planned_hours=8,
            actual_hours=7,
            budget=1200.00,
            sells=1100.00
        )

    def test_get_report_list(self):
        response = self.client.get(reverse('report-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_reports_by_date(self):
        response = self.client.get(reverse('report-list') +
                                   '?date__gte=2024-05-12&date__lte=2024-05-17')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_reports_by_wrong_date(self):
        response = self.client.get(reverse('report-list') +
                                   '?date__gte=2024-05-10&date__lte=2024-05-11')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_filter_reports_by_restaurant(self):
        response = self.client.get(reverse('report-list') +
                                   '?restaurant=Test Restaurant')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_reports_by_restaurant_missing(self):
        response = self.client.get(reverse('report-list') +
                                   '?restaurant=Missing Test Restaurant')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_aggregation(self):
        response = self.client.get(reverse('report-list'))
        self.assertEqual(response.status_code, 200)

        # Check if the data is properly aggregated
        self.assertEqual(len(response.data['results']), 2)

        # Check the aggregated data for the first result

        result_1 = response.data['results'][0]
        self.assertEqual(result_1['date'], '2024-05-13')
        self.assertEqual(result_1['restaurant'], 'Test Restaurant 2')
        self.assertEqual(result_1['total_planned_hours'], 8)
        self.assertEqual(result_1['total_actual_hours'], 7)
        self.assertEqual(result_1['total_budget'], "1200.00")
        self.assertEqual(result_1['total_sells'], "1100.00")

        result_2 = response.data['results'][1]
        self.assertEqual(result_2['date'], '2024-05-16')
        self.assertEqual(result_2['restaurant'], 'Test Restaurant')
        self.assertEqual(result_2['total_planned_hours'], 16)
        self.assertEqual(result_2['total_actual_hours'], 13)
        self.assertEqual(result_2['total_budget'], "2000.00")
        self.assertEqual(result_2['total_sells'], "1800.00")
