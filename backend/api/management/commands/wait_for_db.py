import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ 
    Tells Django to pause execution until database connection is established
    """
    def handle(self, *args, **options):
        self.stdout.write('Waiting for db...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Db unavaible. Waiting 1 sec...')
                time.sleep(1)