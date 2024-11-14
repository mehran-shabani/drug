#drug/urls.py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/drugs/', include('search_drug.roots')),  # اضافه کردن آدرس‌های API اپلیکیشن search_drug
]
