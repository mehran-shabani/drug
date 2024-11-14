# search_drug/serializers.py
from rest_framework import serializers
from .models import Drug

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id', 'generic_name_eng', 'generic_name_fa', 'drug_brand', 'shape_of_drug', 'drug_dose', 'ATC_code']