# search_drug/models.py
from django.db import models


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
    drugs = models.ManyToManyField(Drug, blank=True)
    prescription_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Order for {self.patient_first_name} {self.patient_last_name} with ID {self.id}"
