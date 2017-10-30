# -*- coding: utf-8 -*-
import xlwt
from openpyxl import Workbook
from docx import Document
from docx.shared import Inches
from scientificWork.models import Publication, UserProfile

font0 = xlwt.Font()
font0.name = 'Times New Roman'
font0.colour_index = 2
font0.bold = True

style0 = xlwt.XFStyle()
style0.font = font0


def print_list_publications_xlsx(c):
    wb = Workbook()
    ws = wb.active

    ws['C1'] = "Publication"
    ws['A1'] = "Authors"

    i = 3
    for x in c:
        ws['C'+str(i)]=x["bookName"]
        ws['A' + str(i)] = x["author"]
        i += 1
    wb.save('scientificWork/static/Publications.xlsx')


def print_list_staff_xlsx(c):
    wb = Workbook()
    ws = wb.active

    ws['A1']='Employee'
    ws['C1']='Type'
    ws['E1']='Academic degree'
    i = 3
    for x in c:
        ws['A' + str(i)]=x["name"]
        ws['C'+str(i)] = x["type"]
        ws['E'+str(i)] = x["academic_degree"]
        i += 1
    wb.save('scientificWork/static/Staff.xlsx')


def print_peport_publications_docx(c):
    document = Document()
    document.add_heading('Publications')
    for x in c:
        str = ''
        str += x["bookName"]
        str += ' ( '
        str += x["author"]
        str += ' )'
        document.add_paragraph(str)
    document.save("scientificWork/static/Publications.docx")


def print_peport_staff_docx(c):
    document = Document()
    document.add_heading('Staff')
    for x in c:
        str = ''
        str += x["name"]
        str += ' ( '
        str += x["type"]
        str += ', '
        str += x["academic_degree"]
        str += ' )'
        document.add_paragraph(str)
    document.save("scientificWork/static/Staff.docx")
