import csv
from django.core.management.base import BaseCommand
from users.models import ProfileDesigner


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('users/management/commands/country.csv', 'r', encoding='utf-8') as f:
            csvreader = csv.reader(f)
            next(csvreader)
            for row in csvreader:
                country = row[0]
                specialization = input(f'Enter specialization for country "{country}": ')
                ProfileDesigner.objects.create(country=country, specialization=specialization)
                self.stdout.write(self.style.SUCCESS(f'Country "{country}" with specialization "{specialization}".'))
