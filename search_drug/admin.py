from django.contrib import admin
from .models import Order, OrderMedication

class OrderMedicationInline(admin.TabularInline):
    model = OrderMedication
    extra = 1  # تعداد فرم‌های اضافی برای اضافه کردن دارو

class OrderAdmin(admin.ModelAdmin):
    list_display = ('patient_first_name', 'patient_last_name', 'patient_national_code', 'disease_name')
    search_fields = ['patient_first_name', 'patient_last_name', 'patient_national_code']
    inlines = [OrderMedicationInline]

    # اضافه کردن فیلد لینک دانلود به صفحه ادمین
    fieldsets = (
        ('اطلاعات بیمار', {
            'fields': ('patient_first_name', 'patient_last_name', 'patient_national_code', 'disease_name', 'prescription_note')
        }),
        ('لینک دانلود نسخه', {
            'fields': ('download_link',)  # این فیلد را برای وارد کردن لینک دستی اضافه می‌کنیم
        }),
    )

    # اضافه کردن لینک دانلود به نمایش لیست سفارشات در پنل ادمین
    def download_link(self, obj):
        return f"<a href='{obj.download_link}' target='_blank'>دانلود نسخه</a>"
    download_link.allow_tags = True
    download_link.short_description = 'لینک دانلود'

# ثبت مدل Order در ادمین
admin.site.register(Order, OrderAdmin)
