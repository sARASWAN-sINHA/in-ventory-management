from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2.errors import OperationalError as PostgresOperationalError
import time


class Command(BaseCommand):
    help = "Command which checks and waits untill DB service is up and ready to accept connections."

    def handle(self, *args, **options):
        db_ready = False
        self.stdout.write("Waiting for database service...")

        while db_ready is not True:
            try:
                self.check(databases=["default"])
                db_ready = True
            except (PostgresOperationalError, OperationalError):
                self.stdout.write(self.style.ERROR("Database connection failed!!! Waiting for 1 sec....") )
                time.sleep(1.0)
        self.stdout.write(self.style.SUCCESS("Connected to database service!!"))