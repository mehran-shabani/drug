# search_drug/models.py
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
        return f"{self.generic_name_eng} ({self.drug_dose})"
    
class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    national_code = models.CharField(max_length=12)
    disease_name = models.CharField(max_length=255)


    def __str__(self):
        return f"Order for {self.first_name} {self.last_name} with ID {self.id}"
    

class OrderMedication(models.Model):
    order = models.ForeignKey(Order, related_name='medications', on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    count = models.IntegerField(blank=True, null=True)
    instructions = models.TextField()
    def __str__(self):
        return f"{self.drug.generic_name_eng} for {self.order.id}"
