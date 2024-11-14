# scripts/load_drugs.py
import csv
import os
import django
from django.conf import settings



# تنظیم پروژه Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# بارگذاری تنظیمات و راه‌اندازی Django
try:
    django.setup()
except django.core.exceptions.ImproperlyConfigured as e:
    print(f"Error in Django setup: {e}")
    exit(1)

from search_drug.models import Drug
def load_drugs_from_csv(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        required_fields = ['generic_name_eng', 'generic_name_fa', 'drug_brand', 'shape_of_drug', 'drug_dose', 'ATC_code']
        missing_fields = [field for field in required_fields if field not in reader.fieldnames]

        if missing_fields:
            print(f"Missing required fields in CSV header: {', '.join(missing_fields)}")
            return

        for row in reader:
            try:
                Drug.objects.create(
                    generic_name_eng=row['generic_name_eng'],
                    generic_name_fa=row['generic_name_fa'],
                    drug_brand=row['drug_brand'],
                    shape_of_drug=row['shape_of_drug'],
                    drug_dose=row['drug_dose'],
                    ATC_code=row['ATC_code'],
                )
            except Exception as e:
                print(f"Error importing row {row}: {e}")
                continue

    print('Successfully loaded drugs into the database')


if __name__ == "__main__":
    file_path = settings.CSV_FILE_PATH
    load_drugs_from_csv(file_path)
