import csv
from django.core.management.base import BaseCommand
from job.models import Skill


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('job/management/commands/skills.csv', 'r', encoding='utf-8') as f:
            csvreader = csv.reader(f)
            next(csvreader)
            for row in csvreader:
                name = row[0]
                Skill.objects.create(name=name)
                self.stdout.write(self.style.SUCCESS(f'Skill "{name}" created.'))
