import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import Report


class Command(BaseCommand):
    help = 'Import data from dataset.csv'

    def handle(self, *args, **kwargs):
        with open('data/dataset.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                Report.objects.create(
                    date=date,
                    restaurant=row['restaurant'],
                    planned_hours=int(row['planned_hours']),
                    actual_hours=int(row['actual_hours']),
                    budget=float(row['budget']),
                    sells=float(row['sells'])
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
