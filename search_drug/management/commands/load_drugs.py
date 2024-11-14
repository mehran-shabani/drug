import pandas as pd
from django.core.management.base import BaseCommand
from search_drug.models import Drug
from django.db import transaction

class Command(BaseCommand):
    help = 'Load drugs from CSV file into the database using pandas'

    def add_arguments(self, parser):
        # Argument for dry run
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate the data loading without saving to the database.'
        )

    def handle(self, *args, **options):
        file_path = 'C:/Users/Bartar/OneDrive/Apps/Desktop/projects/drugs_medogram/drug/search_drug/management/commands/drugs.csv'
        dry_run = options['dry_run']
        
        try:
            # خواندن فایل CSV با استفاده از pandas
            df = pd.read_csv(file_path, encoding='utf-8')

            # بررسی اینکه تمام ستون‌های مورد نیاز وجود دارند
            required_columns = ['generic_name_eng', 'generic_name_fa', 'drug_dose']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                self.stdout.write(self.style.ERROR(f"CSV file is missing these required columns: {missing_columns}"))
                return

            # حذف ردیف‌هایی که فیلدهای ضروری آن‌ها خالی است
            initial_row_count = len(df)
            df = df.dropna(subset=['generic_name_eng', 'generic_name_fa', 'drug_dose'])
            cleaned_row_count = len(df)
            removed_rows = initial_row_count - cleaned_row_count

            if removed_rows > 0:
                self.stdout.write(self.style.WARNING(f"{removed_rows} rows were removed due to missing required fields."))

            # ایجاد لیستی از اشیاء Drug برای ذخیره در دیتابیس
            drugs_to_create = []
            for _, row in df.iterrows():
                # تابع strip() فقط برای رشته‌ها استفاده می‌شود
                def safe_strip(val):
                    if isinstance(val, str):
                        return val.strip()
                    return val

                drug = Drug(
                    generic_name_eng=safe_strip(row.get('generic_name_eng')),
                    generic_name_fa=safe_strip(row.get('generic_name_fa')),
                    drug_brand=safe_strip(row.get('drug_brand')) or None,
                    shape_of_drug=safe_strip(row.get('shape_of_drug')) or None,
                    drug_dose=safe_strip(row.get('drug_dose')) or None,
                    ATC_code=safe_strip(row.get('ATC_code')) or None
                )
                drugs_to_create.append(drug)

            # Dry run: فقط نمایش تعداد رکوردهایی که وارد می‌شدند
            if dry_run:
                self.stdout.write(self.style.WARNING(f"Dry run completed. {len(drugs_to_create)} records would have been inserted."))
            else:
                # ذخیره اطلاعات در دیتابیس
                if drugs_to_create:
                    with transaction.atomic():
                        Drug.objects.bulk_create(drugs_to_create)
                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(drugs_to_create)} drugs into the database.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found. Please check the path."))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR(f"CSV file is empty or corrupted."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))