from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils import create_prescription, send_sms_with_kavehnegar
from django.conf import settings
import os

User = get_user_model()

@receiver(post_save, sender=Order)
def create_pdf_and_send_sms(sender, instance, created, **kwargs):
    """
    سیگنالی که بعد از ایجاد یا به‌روزرسانی سفارش، یک فایل PDF می‌سازد و لینک دانلود را برای کاربر ارسال می‌کند.
    """
    if created:
        # سفارش جدید ایجاد شده است
        order = instance
        patient_first_name = order.patient_first_name
        patient_last_name = order.patient_last_name
        patient_national_code = order.patient_national_code
        disease_name = order.disease_name

        # ساخت لیست داروها
        medications = [
            f"{med.drug.generic_name_eng} {med.drug.drug_dose} - {med.instructions}"
            for med in order.medications.all()
        ]

        # لینک تأیید (بر اساس کد ملی)
        verification_url = f"http://example.com/verify/{patient_national_code}"

        # ساخت فایل PDF نسخه
        pdf_success = create_prescription(
            patient_first_name,
            patient_last_name,
            patient_national_code,
            disease_name,
            medications,
            verification_url
        )

            