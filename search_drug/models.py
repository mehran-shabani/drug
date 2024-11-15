# search_drug/models.py
import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Drug(models.Model):
    generic_name_eng = models.CharField(max_length=255)
    generic_name_fa = models.CharField(max_length=255)
    drug_brand = models.CharField(max_length=255, null=True, blank=True)
    shape_of_drug = models.CharField(max_length=255, null=True, blank=True)
    drug_dose = models.CharField(max_length=255, null=True, blank=True)  # اجازه NULL و خالی
    ATC_code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.generic_name_eng} ({self.generic_name_fa})"
    
class Order(models.Model):
    patient_first_name = models.CharField(max_length=255)
    patient_last_name = models.CharField(max_length=255)
    patient_national_code = models.CharField(max_length=12)
    disease_name = models.CharField(max_length=255)
    prescription_note = models.TextField(null=True, blank=True)
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False)  # فیلد کد تأیید
    download_link = models.URLField(null=True, blank=True)  # لینک دانلود نسخه



    def clean(self):
        if self.order.medications.count() > 10:
            raise ValidationError('Each order can only contain a maximum of 10 medications.')

    def __str__(self):
        return f"Order for {self.patient_first_name} {self.patient_last_name} with ID {self.id}"
    

class OrderMedication(models.Model):
    order = models.ForeignKey(Order, related_name='medications', on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    instructions = models.TextField()  # مثلاً نحوه مصرف

    def __str__(self):
        return f"{self.drug.generic_name_eng} for {self.order.id}"
