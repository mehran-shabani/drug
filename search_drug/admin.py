from django.contrib import admin
from .models import Order, OrderMedication
from .utils import create_prescription

class OrderMedicationInline(admin.TabularInline):
    model = OrderMedication
    extra = 1 

class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'national_code', 'disease_name')
    actions = ['generate_pdf']  # اضافه کردن اکشن به لیست اکشن‌ها
    search_fields = ['first_name', 'last_name', 'national_code']
    inlines = [OrderMedicationInline]

    fieldsets = (
        ('اطلاعات بیمار', {
            'fields': ('first_name', 'last_name', 'national_code', 'disease_name')
        }),
    )
    
    def generate_pdf(self, request, queryset):
        for order in queryset:
            first_name = order.first_name
            last_name = order.last_name
            national_code = order.national_code
            disease_name = order.disease_name

            # ساخت لیست داروها
            medications = [
                f"{(med.drug.generic_name_eng).lower()}({med.drug.drug_dose}) - {med.instructions} {med.count}"
                for med in order.medications.all()
            ]
            
            verification_url = f"https://api.medogram.ir/api/order/verification/{order.national_code}"

            # ایجاد فایل PDF نسخه
            create_prescription(
                first_name,
                last_name,
                national_code,
                disease_name,
                medications,
                verification_url
            )
            # پیام موفقیت در ادمین
            self.message_user(request, f"PDF for order {order.id} created successfully.")

    generate_pdf.short_description = "Generate pdf" 

# ثبت مدل در ادمین
admin.site.register(Order, OrderAdmin)
