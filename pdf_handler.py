#============================= PDF HANDLER =============================#
#                                                                       #
# Program that allows you to work with PDF files in the following ways: #
#                                                                       #
#           * Merge files.                                              #
#           * Extract one or more sheets from a file.                   #
#           * Lower the file size (It is not always possible).          #
#           * Encrypt a file.                                           #
#                                                                       #
#=======================================================================#

from tkinter.font import Font
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pathlib
from tkinter.ttk import Separator
from typing import Literal
from PyPDF2 import PdfMerger, PdfFileWriter, PdfFileReader
import os
from PIL import ImageTk
from base64 import b64decode
import icon64


# Auxiliary function in case of failed urls
def replace_slash(files):

    ficheros=[]

    for i in files:

        pth=pathlib.Path(i)
        pth=str(pth)
        ficheros.append(pth.replace('/', '\\'))

    return ficheros


# Function to select PDF(s)
def seleccionar_pdf(num_pdfs: Literal['uno','varios']):

    if num_pdfs == 'varios':

        file_path = filedialog.askopenfilenames(title="Select PDF", initialdir="C:", filetypes=(("PDF files", "*.pdf"),))
        file_path = list(file_path)
    elif num_pdfs == 'uno':

        file_path = filedialog.askopenfilename(title="Select PDF", initialdir="C:", filetypes= (("PDF files", "*.pdf"),))
    else:
        pass

    return file_path


# Function to save the new PDF
def guardar_pdf(nuevo):

    work_file = os.path.dirname(__file__) # Save the path of the working folder (where the '.py' file is located).
    all_files = os.listdir(work_file) # Saves all the files in the folder in a list.
    destination = ''.join(replace_slash(work_file)) # Where the file will be saved

    aux_root= Tk()
    aux_root.resizable(0,0)
    aux_root.title('Save file')

    aux_mf= Frame(aux_root)
    aux_mf.pack()

    def save_file():

        if ent.get()== '':
            nom = 'file_doe'
        else:
            nom= ent.get()


        if '.pdf' in ent.get():
            nom= ent.get().replace('.pdf', '')   


        if nom + '.pdf' in all_files:
            nom= nom + '-new'


        with open(f'{destination}\\{nom}.pdf', 'wb') as new_file:
            nuevo.write(new_file)
        
        messagebox.showinfo(title= 'Saved', message= f'File saved successfully.'
            f'\n\nFile name: {nom}.pdf'
            f'\n\nFile path: {destination}')

        aux_root.destroy()

    entVar= StringVar()

    lb= Label(aux_mf, text= 'Select the file name:', font= 'bold', pady= 15, padx= 30)
    lb.grid(row= 0, column= 0)

    ent= Entry(aux_mf, textvariable= entVar)
    ent.grid(row= 1, column= 0, pady= 15)

    btn= Button(aux_mf, text= 'Send', pady= 5, font= 'bold', activebackground= "#38EB5C", cursor= 'hand2', bd= 5,width= 10,command= save_file)
    btn.grid(row= 2, column= 0)

    aux_root.mainloop()


# Function that merge selected PDFs
def merge_files():

    file_path= seleccionar_pdf('varios')
    lst_pdf= file_path

    merge = PdfMerger()

    if len(lst_pdf) != 0:
        for pdf in lst_pdf:
            merge.append(pdf)

        guardar_pdf(merge)
    else:
        pass


# Function to extract sheets from a PDF. One or several.
def extract_sheets():

    def parametros(hoja_inicio, hoja_final, writer, reader, root):

        root.destroy()

        if hoja_inicio > hoja_final-1:
            messagebox.showerror(title= 'ERROR', message= 'The Start Sheet can NOT be larger than the End Sheet.')
        else:
            for i in range(hoja_inicio,hoja_final):
                writer.addPage(reader.getPage(i))

            guardar_pdf(writer)

    try:
        reader=PdfFileReader(seleccionar_pdf('uno'),strict=False)
        writer = PdfFileWriter()
        
        aux_root=Tk()
        aux_mf=Frame(aux_root)
        aux_root.title('Parameters')

        aux_mf.pack(fill= 'both', expand= 1)
        aux_mf.config(padx= 50, pady= 50)

        hoja_1Var=IntVar()
        hoja_2Var=IntVar()

        lb1= Label(aux_mf, text= 'Start sheet:', font= 'bold')
        lb1.grid(row= 1, column= 0)

        et1= Spinbox(aux_mf, textvariable= hoja_1Var, from_=0, to= reader.getNumPages(), wrap= True)
        et1.grid(row= 1, column= 1, pady= 25)
        et1.config(font= Font(family= 'Helvetica', size= 25, weight= 'bold'))

        lb2= Label(aux_mf, text= 'End sheet:', font= 'bold')
        lb2.grid(row= 2, column= 0)

        et2= Spinbox(aux_mf, textvariable= hoja_2Var, from_=0, to= reader.getNumPages(), wrap= True)
        et2.grid(row= 2, column= 1, pady= 25)
        et2.config(font= Font(family= 'Helvetica', size= 25, weight= 'bold'))

        bt= Button(aux_mf, text= 'Send', font= 'bold', activebackground= "#38EB5C", cursor= 'hand2', command= lambda: parametros(int(et1.get()), int(et2.get())+1, writer, reader, aux_root))
        bt.grid(row= 3, columnspan= 2)
        bt.config(padx= 10, pady= 10, bd= 5)

        aux_root.mainloop()
    except:
        pass

    
# Function to resize the PDF 
def resize():

    try:
        reader=PdfFileReader(seleccionar_pdf('uno'),strict=False)
        writer = PdfFileWriter()

        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)

        guardar_pdf(writer)
    except:
        pass


# Function to add watermark to PDF in all sheets
def watermark_adder():

    try:
        watermark= PdfFileReader(filedialog.askopenfilename(title= "Select watermark", initialdir= "C:", filetypes= (("PDF files", "*.pdf"),)))
        watermark= watermark.getPage(0)

        reader= PdfFileReader(seleccionar_pdf('uno'), strict= False)
        writer= PdfFileWriter()

        for i in range(reader.getNumPages()):
            page= reader.getPage(i)
            page.mergePage(watermark)
            writer.addPage(page)

        guardar_pdf(writer)
    except:
        pass


# Function to encrypt a PDF
def encrypt_pdf():

    try:
        reader = PdfFileReader(seleccionar_pdf('uno'), strict= False)
        writer = PdfFileWriter()

        for page in reader.pages:
            writer.addPage(page)

        writer.encrypt("1234")

        guardar_pdf(writer)
    except:
        pass


###~~ Main ~~###

if __name__ == '__main__':

    root=Tk()
    
    try:
        icon_img = icon64.icono()

        icon_img = b64decode(icon_img)
        icon_img = ImageTk.PhotoImage(data= icon_img)
        root.tk.call('wm', 'iconphoto', root._w, icon_img)
    except:
        pass

    root.title("PDF HANDLER")
    root.resizable(0,0)

    mf1=Frame(root)
    mf1.pack(fill= 'both', expand= 1, padx= 80, pady= 0)

    mf2=Frame(root)
    mf2.pack(fill= 'both', expand= 1, padx= 80, pady= 0)

    # Header
    app_header= Label(mf1, text= 'PDF HANDLER', font= 'bold', highlightthickness= 3, highlightbackground= 'blue', width= 26, bg= 'white')
    app_header.grid(row= 0, columnspan= 3, pady= 20)


    # First Line
    merged_button= Button(mf1, text= 'Merge', font= 'bold', activebackground= "#38EB5C", cursor= 'hand2', width= 13, command= merge_files)
    merged_button.grid(row= 1, column= 0, pady=15)
    merged_button.config(padx= 10, pady= 10, bd= 5)

    sep=Separator(mf1, orient= 'vertical')
    sep.grid(row= 1, column= 1, sticky= 'ns', padx= 20)

    extract_button= Button(mf1, text= 'Extract Sheets', font= 'bold', activebackground= "#38EB5C", cursor= 'hand2', width= 13, command= extract_sheets)
    extract_button.grid(row= 1, column= 2, pady=15)
    extract_button.config(padx= 10, pady= 10, bd= 5)

    sep= Separator(mf1, orient= 'horizontal')
    sep.grid(row=2, columnspan= 3, sticky= 'ew', pady= 5)


    # Second Line
    resize_button= Button(mf1, text= 'Resize PDF', font= 'bold', activebackground= "#38EB5C", cursor= 'hand2', width= 13, command= resize)
    resize_button.grid(row= 3, column= 0, pady=15)
    resize_button.config(padx= 10, pady= 10, bd= 5)

    sep= Separator(mf1, orient= 'vertical')
    sep.grid(row= 3, column= 1, sticky= 'ns', padx= 20)

    water_button= Button(mf1, text= 'Watermark', font= 'bold', activebackground= "#38EB5C", cursor= 'hand2', width= 13, command= watermark_adder)
    water_button.grid(row= 3, column= 2, pady=15)
    water_button.config(padx= 10, pady= 10, bd= 5)

    sep= Separator(mf1, orient= 'horizontal')
    sep.grid(row=4, columnspan= 3, sticky= 'ew', pady= 5)


    # Last Line 
    encrypt_button= Button(mf2, text= 'Encrypt PDF', font= 'bold', activebackground= "#38EB5C", cursor= 'hand2', width= 13, command= encrypt_pdf)
    encrypt_button.pack( pady=15)
    encrypt_button.config(padx= 10, pady= 10, bd= 5)


    root.mainloop()
