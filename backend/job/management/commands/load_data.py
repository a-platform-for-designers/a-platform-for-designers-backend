import csv
from django.core.management.base import BaseCommand
from job.models import Specialization, Language, Skill, Sphere, Instrument

SOURCE_MODEL = {
    'job/management/commands/direction.csv': Specialization,
    'job/management/commands/languages.csv': Language,
    'job/management/commands/skills.csv': Skill,
    'job/management/commands/sphere.csv': Sphere,
    'job/management/commands/tools.csv': Instrument
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for source, model in SOURCE_MODEL.items():
            with open(source, 'r', encoding='utf-8') as f:
                csvreader = csv.reader(f)
                next(csvreader)
                for row in csvreader:
                    name = row[0]
                    model.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f'{model} "{name}" created.'))
