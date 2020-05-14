import base64
from docxtpl import DocxTemplate

with open('C:\\xampp\\htdocs\\pdftotext\\base64.txt', 'r') as file:
    data = file.read() #.replace('\n', '')

#print(b64decode(data)) #-> 'guru'

decoded = base64.b64decode(data)


from io import BytesIO
from zipfile import ZipFile
import os

fp = BytesIO(decoded)

with open("C:\\xampp\\htdocs\\pdftotext\\basetest.docx", "wb") as f:
    f.write(fp.getbuffer())

#zfp = ZipFile(fp, "r")
#zfp.extractall('C:\\xampp\\htdocs\\pdftotext\\zip')

#zfp.printdir()