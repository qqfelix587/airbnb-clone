from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "this command creates house rules"

    """def add_arguments(self, parser):

        parser.add_argument(
            "--times",
            help="How many times do you want me to tell you that I love you?",
        )"""

    def handle(self, *args, **options):
        house_rules = [
            "No parties or events allowed.",
            "No smoking allowed. ",
            "No pets allowed.",
            "Suitable for toddlers and children under 12.",
            "No unregistered guests allowed. ",
            "Please don’t eat or drink in the bedrooms. ",
            "Please respect the noise curfew. ",
            "Please turn off the AC when you go out.",
            "Please respect check-in and check-out times. ",
            "Please take extra care of your keys. Lost keys incur a replacement fee.",
            "Please take care of the furnishings. You have to pay for damages that exceed the security deposit. ",
            "Please don’t rearrange the furniture.",
            "Please do your dishes.",
            "Please take the trash out before you leave.",
            "No illegal substances allowed on the premises.",
        ]
        for a in house_rules:
            room_models.HouseRule.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("House Rules created!"))
