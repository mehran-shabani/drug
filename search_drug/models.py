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
