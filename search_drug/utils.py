import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import jdatetime
import io
from PIL import Image
import qrcode
import logging

def binary_generator():
    image_path = os.path.join(os.path.dirname(__file__), 'logo.png')
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
    return binary_data

def create_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="#4682B4", back_color="white")
    temp_qr_path = "temp_qr.png"
    qr_image.save(temp_qr_path)
    return temp_qr_path

def create_prescription(first_name, last_name, national_code, sick_name, medications, verification_url):
    try:
        output_dir = os.path.join('media/pdf')  # مسیر ذخیره‌سازی فایل

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_name = os.path.join(output_dir, f'prescription_{national_code}.pdf')
        
        width, height = A4
        margin = 40
        
        c = canvas.Canvas(file_name, pagesize=A4)

        # کادر بیرونی با ارتفاع بیشتر
        c.setStrokeColor(colors.HexColor('#4682B4'))
        c.setLineWidth(2)
        c.roundRect(margin, margin, width - 2 * margin, height - 2 * margin, 15)

        # کادر داخلی تزئینی
        inner_margin = margin + 10
        c.setStrokeColor(colors.HexColor('#B0C4DE'))
        c.setLineWidth(1)
        c.roundRect(inner_margin, inner_margin, width - 2 * inner_margin, height - 2 * inner_margin - 20, 15)
        
        # لوگو در بالای صفحه
        logo_data = binary_generator()
        with Image.open(io.BytesIO(logo_data)) as img:
            temp_logo_path = "temp_logo.png"
            img.save(temp_logo_path)

            logo_width = 100
            logo_height = 60
            logo_x = (width - logo_width) / 2
            logo_y = height - margin - 60

            c.drawImage(temp_logo_path, logo_x, logo_y, width=logo_width, height=logo_height)
            os.remove(temp_logo_path)

        # نوار تزئینی بالای صفحه
        c.setFillColor(colors.HexColor('#4682B4'))
        c.rect(margin, height - margin - 80, width - 2 * margin, 15, fill=1)

        # عنوان
        c.setFont('Helvetica', 22)
        c.setFillColor(colors.HexColor('#1E4F78'))
        title = "Medical Prescription"
        c.drawCentredString(width / 2, height - margin - 120, title)

        # خطوط تزئینی زیر عنوان
        c.setStrokeColor(colors.HexColor('#4682B4'))
        c.setLineWidth(1.5)
        title_underline_y = height - margin - 130
        c.line(width / 3, title_underline_y, width * 2 / 3, title_underline_y)

        # محتوای اصلی
        content_start_y = height - margin - 180
        line_height = 30

        c.setFont('Helvetica', 12)
        c.setFillColor(colors.black)

        # اطلاعات بیمار - در دو ستون
        right_column = [
            f"Last Name: {last_name}",
            f"Date: {jdatetime.date.today().strftime('%Y/%m/%d')}",
            f"National Code: {national_code}",
        ]

        left_column = [
            f"First Name: {first_name}",
            f"Prescription No: {jdatetime.datetime.now().strftime('%Y%m%d%H%M')}",
            "",
        ]

        # چاپ ستون راست
        for i, text in enumerate(right_column):
            y_pos = content_start_y - (i * line_height)
            c.drawRightString(width - inner_margin - 10, y_pos, text)

        # چاپ ستون چپ
        for i, text in enumerate(left_column):
            y_pos = content_start_y - (i * line_height)
            c.drawRightString(width / 2 + 50, y_pos, text)

        # اطلاعات بیماری
        c.setFont('Helvetica', 12)
        disease_info = f"Disease Name: {sick_name}"
        c.drawCentredString(width / 2, content_start_y - 3.5 * line_height, disease_info)

        # چاپ اطلاعات داروها
        med_start_y = content_start_y - 5 * line_height
        if len(medications) <= 3:
            for i, med in enumerate(medications):
                med_text = med
                c.drawCentredString(width / 2, med_start_y - (i * line_height), med_text)
        else:
            first_column_meds = medications[:len(medications) // 2]
            second_column_meds = medications[len(medications) // 2:]
            
            for i, med in enumerate(first_column_meds):
                med_text = med
                y_pos = med_start_y - (i * line_height)
                c.drawRightString(width / 2 - 20, y_pos, med_text)

            for i, med in enumerate(second_column_meds):
                med_text = med
                y_pos = med_start_y - (i * line_height)
                c.drawRightString(width - inner_margin - 20, y_pos, med_text)

        # اطلاعات پزشک در بالای امضا
        c.setFont('Helvetica', 12)
        doctor_info = "Dr. Shabani Shahreza 168396"
        c.drawRightString(width - inner_margin - 10, margin + 250, doctor_info)

        # جای امضا
        signature_image_path = os.path.join(os.path.dirname(__file__), 'logo1.png')
        c.drawImage(signature_image_path, width - inner_margin - 300, margin + 160, width=100, height=60)

        # QR code
        qr_path = create_qr_code(verification_url)
        qr_size = 80
        qr_x = (width - qr_size) / 2
        qr_y = margin + 50   #به پایین منتقل شده است
        c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
        os.remove(qr_path)

        # متن راهنمای QR
        c.setFont('Helvetica', 9)
        c.setFillColor(colors.HexColor('#1E4F78'))
        qr_guide = "Scan the QR code to verify the prescription."
        c.drawCentredString(width / 2, qr_y - 15, qr_guide)

        # متن پایین صفحه
        c.setFont('Helvetica', 11)
        footer_text = "Medogram Visit Online"
        c.drawCentredString(width / 2, margin + 20, footer_text)

        c.save()
        print(f'OK file: {file_name} created')

        return True

    except Exception as e:
        logging.error(f"Error in creating PDF for {national_code}: {str(e)}")
        return False

