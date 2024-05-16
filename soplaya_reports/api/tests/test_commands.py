from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from api.models import Report


class ImportDataCommandTestCase(TestCase):
    def test_import_data(self):
        out = StringIO()
        call_command('import_data', stdout=out)
        self.assertIn('Data imported successfully', out.getvalue())
        self.assertEqual(Report.objects.count(), 6000)
