## pdf report maker file

# Inspired from the original Pdf_report_maker.ipynb file,
# but only retaining the functions that are not already integrate elsewhere

from reportlab.pdfgen import canvas
from Read_TXT_SNRs import read_txt_snrs
import os


def create_pdf_report(root_dir, log=print):
    pdf_path = os.path.join(root_dir, "overview.pdf")
    pdf = canvas.Canvas(pdf_path, pagesize=(805, 1110))
    pdf.drawString(50, 1050, root_dir)

    pages = 0
    for root, _, files in os.walk(root_dir):
        file_set = set(files)
        has_a = "ChanA_stk_avg.tif" in file_set
        has_b = "ChanB_stk_avg.tif" in file_set
        if not (has_a or has_b):
            continue

        pdf.showPage()
        pages += 1
        pdf.drawString(50, 1050, root)
        if has_a:
            _draw_channel(pdf, root, "ChanA", image_x=50, title_x=150, snr_x=150)
        if has_b:
            _draw_channel(pdf, root, "ChanB", image_x=400, title_x=450, snr_x=450)

    pdf.save()
    log(f"PDF pages written: {pages + 1} (cover + {pages} recording page(s))")
    return pdf_path


def _draw_channel(pdf, folder, chan, image_x, title_x, snr_x):
    tif_name = f"{chan}_stk_avg.tif"
    png_path = os.path.join(folder, f"{chan}_stk_avg.png")
    tif_path = os.path.join(folder, tif_name)
    ft_snr, snr = read_txt_snrs(tif_path)

    pdf.drawString(title_x, 980, chan.replace("Chan", "Chan "))
    if os.path.isfile(png_path):
        pdf.drawImage(png_path, image_x, 700, width=350, height=260)
    else:
        pdf.drawString(image_x, 800, f"Missing preview: {os.path.basename(png_path)}")
    pdf.drawString(snr_x, 600, f"SNR = {snr}")
    pdf.drawString(snr_x, 550, f"SNR = {ft_snr}")
