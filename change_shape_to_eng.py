import sqlite3

# اتصال به پایگاه داده SQLite (جایگذاری نمایید با مسیر فایل خود)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# دیکشنری معادل‌های جدید برای هر نوع دارو
replacement_dict = {
    "قرص": "Tab",
    "شیاف": "Supp",
    "شربت": "Syrup",
    "قطره خوراکی": "Oral Drop",
    "سوسپانسیون": "Susp",
    "آمپول": "Amp",
    "قرص جوشان": "Eff Tab",
    "ویال": "Vial",
    "پماد چشمی": "Eye Ointment",
    "کرم موضعی": "Topical",
    "کپسول": "Cap",
    "قطره چشمی": "Eye Drop",
    "پودر": "Powder",
    "اسپری بینی": "Spray",
    "اسپری تنفسی": "Inhale Spray",
    "دهانشویه": "Mouth Wash",
    "لوسیون موضعی": "Topical Lotion",
    "پماد": "Ointment",
    "کرم": "Cream",
    "الگزیر": "Elixir",
    "محلول استنشاقی": "Inhalation Susp",
    "پودر استنشاقی": "Inhalation Powder",
    "کرم جلدی": "Topical Cream",
    "پماد جلدی": "Top Ointment",
    "پودر خوراکی": "Oral Powder",
    "محلول تزریقی": "Injection Susp",
    "nan": "Nan",
    "کرم واژینال": "Vaginal Cream",
    "محلول": "Susp",
    "لوسیون": "Lotion",
    "محلول موضعی": "Top Susp",
    "قرص واژینال": "Vaginal Tab",
    "سرم تزریقی": "Serum",
    "رکتال تیوب": "Rectal Tube",
    "ژل": "Gel",
    "آمپول آماده تزریق": "Ampule",
    "اینهالر": "Inhaler",
    "کپسول استنشاقی": "Inhaler Cap",
    "شامپو": "Shampoo",
    "پرل": "Pearl",
    "قلم تزریقی": "Insulin Pen",
    "اسپری": "Spray",
    "قطره بینی": "Nasal Drop",
    "قطره": "Drop",
    "کپسول واژینال": "Vaginal Cap",
    "محلول حجمی": "Susp",
    "اسپری دهانی": "Oral Spray",
    "فرآورده پودری": "Powder Drug",
    "قرص جویدنی": "Chewable Tab",
    "جوشان": "Effortless",
}

# اعمال تغییرات بر روی پایگاه داده
for original_shape, new_value in replacement_dict.items():
    cursor.execute("UPDATE search_drug_drug SET shape_of_drug = ? WHERE shape_of_drug = ?", (new_value, original_shape))

# اعمال و بستن اتصال
conn.commit()
conn.close()

print("تمام تغییرات با موفقیت اعمال شد.")
