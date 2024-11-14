from rest_framework import generics
from .models import Drug
from .serializers import DrugSerializer
from django.db.models import Q

class DrugSearchView(generics.ListAPIView):
    serializer_class = DrugSerializer  # استفاده از سریالایزر اصلی

    def get_queryset(self):
        query = self.request.query_params.get('q', '')  # دریافت پارامتر جستجو
        if query:
            return Drug.objects.filter(
                Q(generic_name_eng__icontains=query) | 
                Q(generic_name_fa__icontains=query)
            ).only('id', 'generic_name_eng')  # فقط فیلدهای id و generic_name_eng واکشی می‌شوند
        return Drug.objects.only('id', 'generic_name_eng')

class DrugDetailView(generics.RetrieveAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    lookup_field = 'id'