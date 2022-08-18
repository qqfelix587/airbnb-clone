from django.core.management.base import BaseCommand
from rooms.models import RoomType 


class Command(BaseCommand):
    help = "This command creates Room Typespipe"

    def handle(self, *args, **options):
        room_types = [
            "Entire Place",
            "Shared Room",
            "Private Room",
            "Hotel"
        ]

        for r in room_types:
            RoomType.objects.create(name=r)

        self.stdout.write(self.style.SUCCESS("RoomTypes created!"))