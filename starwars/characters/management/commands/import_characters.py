import json

from django.core.management.base import BaseCommand

from starwars.characters.models import Character, Team
from starwars.characters.utils import import_characters


class Command(BaseCommand):

    help = 'Import character data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        # option to do data analysis
        parser.add_argument(
            '--analysis',
            action='store_true',
            help='Perform data analysis on the imported data',
        )
        # option to reset the data
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset the data before importing',
        )

    def data_analysis(self, characters):
        """
        Find out all the attributes of the characters in the data.
        We will store the attributes who have the most occurrences.
        With the exception to the important relationships like masters and
        apprentices.
        """

        keys = []
        key_count = {}
        for character in characters:
            keys += character.keys()
            for key in character.keys():
                key_count[key] = key_count.get(key, 0) + 1

        keys = set(keys)
        # sort by count
        keys = sorted(keys, key=lambda x: key_count[x], reverse=True)

        for key in keys:
            print(f"{key}: {key_count[key]}")

    def handle(self, *args, **options):
        # Run the analysis
        if options['analysis']:
            with open(options['file']) as f:
                characters = json.load(f)
                self.data_analysis(characters)
            return

        if options['reset']:
            Character.objects.all().delete()
            Team.objects.all().delete()

        file = options['file']
        with open(file) as f:
            characters = json.load(f)
            import_characters(characters)
