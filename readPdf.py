
# importing required modules
from PyPDF2 import PdfReader
 
# creating a pdf reader object
reader = PdfReader(r'C:\Users\Abhishek K\Desktop\soup\actual_task\sample.pdf')
 
# printing number of pages in pdf file
print(len(reader.pages))
 
# getting a specific page from the pdf file
page = reader.pages[0]



