from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import datetime
import PIL
from PIL import Image

def generate_report(filename: str, document_title: str, title:str, images: list, textlines: list):
    pdf = canvas.Canvas(filename=f"report/{filename}_{datetime.datetime.timestamp(datetime.datetime.now())}.pdf")
    pdf.setTitle(document_title)
    pdf.setFont('Courier-Bold', 14)
    pdf.drawCentredString(300, 770, title)

    pdf.setFont("Courier", 8)
    pdf.drawCentredString(300, 740, "By Caio Madeira")

    pdf.line(30, 730, 550, 730)
    
    img_x = 5
    img_y = 350
    for i, image in enumerate(images):
        pdf.drawInlineImage(image, img_x, img_y, 590, 350) 

    text = pdf.beginText(20, img_y - 40)
    text.setFont("Courier", 10)
    text.setFillColor(colors.black)
        
    for line in textlines:
        text.textLine(line)
        
    pdf.drawText(text)
    
    pdf.save()