from django.core.management.base import BaseCommand
from depreciation.models import Vehicle  
import MySQLdb

class Command(BaseCommand):
    help = 'Load data from motorcycle_info table into Vehicle model'

    def handle(self, *args, **options):
        # Database connection settings
        db = MySQLdb.connect(
            host="localhost", 
            user="root",  
            passwd="password",
            db="motors_dummy"
        )
        cursor = db.cursor()

        # Query motorcycle_info table
        cursor.execute(
            "SELECT maker, model, transmission, year, odometer_reading, price FROM motorcycle_info")
        rows = cursor.fetchall()

        for row in rows:
            maker, model, transmission, year, odometer, price = row
            transmission = transmission if transmission else 'Manual'
            year = year if year else 2019
            Vehicle.objects.update_or_create(
                model=model,
                maker=maker,
                defaults={
                    'odometer': odometer,
                    'price': price,
                    'transmission': transmission,
                    'year': year
                }
            )

        db.close()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
