# search_drug/management/commands/load_drugs.py

import csv
from django.core.management.base import BaseCommand
from search_drug.models import Drug  # مسیر دقیق فایل مدل‌ها

class Command(BaseCommand):
    help = 'Load drugs from CSV file into the database'

    def handle(self, *args, **kwargs):
        file_path = 'C:/Users/Bartar/OneDrive/Apps/Desktop/projects/drugs_medogram/drug/search_drug/management/commands/drugs.csv'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Drug.objects.create(
                        generic_name_eng=row.get('generic_name_eng', ''),
                        generic_name_fa=row.get('generic_name_fa', ''),
                        drug_brand=row.get('drug_brand', ''),
                        shape_of_drug=row.get('shape_of_drug', ''),
                        drug_dose=row.get('drug_dose', ''),
                        ATC_code=row.get('ATC_code', ''),
                    )
            self.stdout.write(self.style.SUCCESS('Successfully loaded drugs into the database'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found. Please check the path."))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Column not found in CSV: {e}"))
