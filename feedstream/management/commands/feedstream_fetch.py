from django.core.management.base import BaseCommand, CommandError
from feedstream.models import Feed

class Command(BaseCommand):
    help = """
    Fetch new items from RSS feeds - I suggest running this every 15 minutes.
    """.strip()
    
    requires_model_validation = True
    can_import_settings = True
    
    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            feed.fetch()
