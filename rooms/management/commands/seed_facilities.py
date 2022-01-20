from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "this command creates facilities"

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            room_models.Facility.objects.create(name=f)

        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))
