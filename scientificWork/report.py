
from docx import Document
from docx.shared import Inches
from scientificWork.models import Publication, UserProfile

def print_peport_publications_docx(c):
    document = Document()
    document.add_heading('Publications')
    for x in c:
        str=''
        str+=x.bookName
        str+=' ( '
        str+=x.user.patronymic
        str+=' )'
        document.add_paragraph(str)
    document.save("scientificWork/static/Publications.docx")

def print_peport_staff_docx(c):
    document = Document()
    document.add_heading('Staff')
    for x in c:
        str=''
        str+=x.patronymic
        str+=' ( '
        str+=x.typestr
        str+=', '
        str+=x.academic_degreestr
        str+=' )'
        document.add_paragraph(str)
    document.save("scientificWork/static/Staff.docx")
