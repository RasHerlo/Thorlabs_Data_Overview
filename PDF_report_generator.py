
## pdf report maker file

# Inspired from the original Pdf_report_maker.ipynb file, 
# but only retaining the functions that are not already integrate elsewhere

from reportlab.pdfgen import canvas
from Read_TXT_SNRs import read_txt_snrs
import os


def create_pdf_report(root_dir):
    pdf = canvas.Canvas(f"{os.path.join(root_dir,'overview')}.pdf", pagesize=(805, 1110))
    # pdf.setFont("Helvetica", 16)
    pdf.drawString(50, 1050, root_dir)
    
    # INSERT AND OVERVIEW OF THE FOLDER STRUCTURE
    # Take a walk through folders, construct "tree-model of data structure?"
    
    
    # Iterate through subdirectories and find .tif files
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith("A_stk_avg.tif"):
                pdf.showPage()
                pdf.drawString(50, 1050, root) 
            #    tif2png(os.path.join(root,'ChanA_stk_avg.tif'), os.path.join(root,'ChanA_stk_avg.png'))
            #    # Calculate snr and ft_snr
                ft_snr, snr = read_txt_snrs(os.path.join(root,'ChanA_stk_avg.tif'))
                pdf.drawImage(os.path.join(root,'ChanA_stk_avg.png'), 50, 700, width=350, height=260)
                pdf.drawString(150, 980, "Chan A")
                pdf.drawString(150, 600, f"SNR = {snr}")
                pdf.drawString(150, 550, f"SNR = {ft_snr}")
            if file.endswith("B_stk_avg.tif"):
            #    tif2png(os.path.join(root,'ChanB_stk_avg.tif'), os.path.join(root,'ChanB_stk_avg.png'))
            #    # Calculate snr and ft_snr
                ft_snr, snr = read_txt_snrs(os.path.join(root,'ChanB_stk_avg.tif'))
                pdf.drawImage(os.path.join(root,'ChanB_stk_avg.png'), 400, 700, width=350, height=260)
                pdf.drawString(450, 980, "Chan B")
                pdf.drawString(450, 600, f"SNR = {snr}")
                pdf.drawString(450, 550, f"SNR = {ft_snr}")
                
            # Insert info regarding correlation between channels

    pdf.save()