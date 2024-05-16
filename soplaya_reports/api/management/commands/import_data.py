import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from api.models import Report


class Command(BaseCommand):
    """Comando per l'importazione dei dati da dataset.csv."""

    help = 'Import data from dataset.csv'

    def handle(self, *args, **kwargs):
        """Gestisce l'importazione dei dati."""
        try:
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
        except (FileNotFoundError, csv.Error, ValidationError) as e:
            self.stdout.write(self.style.ERROR(f'Error during data import: {str(e)}'))
            return
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
