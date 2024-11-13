from django.db import models

class Drug(models.Model):
    generic_name_eng = models.CharField(max_length=100)
    generic_name_fa = models.CharField(max_length=100)
    drug_brand = models.CharField(max_length=100, null=True, blank=True)
    shape_of_drug = models.CharField(max_length=50)
    drug_dose = models.CharField(max_length=50)
    ATC_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.generic_name_eng} ({self.generic_name_fa})"

