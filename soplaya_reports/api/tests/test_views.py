from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Report


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

    def test_get_report_list(self):
        response = self.client.get(reverse('report-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_reports_by_date(self):
        response = self.client.get(reverse('report-list') +
                                   '?date__gte=2024-05-15&date__lte=2024-05-17')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

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
