import os
import base64
from docxtpl import DocxTemplate

with open('C:\\xampp\\htdocs\\pdftotext\\base64.txt', 'r') as file:
    data = file.read() #.replace('\n', '')

#print(b64decode(data)) #-> 'guru'

decoded = base64.b64decode(data)


from io import BytesIO
from zipfile import ZipFile

fp = BytesIO(decoded)
zfp = ZipFile(fp, "r")

print(zfp)

archive_name = 'base.doc'
    # below one line of code will create a 'Zip' in the current working directory
with ZipFile(archive_name, 'w') as file:
  print("{} is created.".format(archive_name))
#zfp.extractall('C:\\xampp\\htdocs\\pdftotext\\zip')
#zfp.printdir()