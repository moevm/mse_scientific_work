# -*- coding: utf-8 -*-
import xlwt
from docx import Document
from docx.shared import Inches
from scientificWork.models import Publication, UserProfile

font0 = xlwt.Font()
font0.name = 'Times New Roman'
font0.colour_index = 2
font0.bold = True

style0 = xlwt.XFStyle()
style0.font = font0


def print_list_publications_xls(c):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Publications')

    ws.write(0, 2, 'Publication', style0)
    ws.write(0, 0, 'Authors', style0)
    i = 1
    for x in c:
        ws.write(i, 2, x.bookName)
        ws.write(i, 0, x.user.patronymic)
        i += 1
    wb.save('scientificWork/static/Publications.xls')


def print_list_staff_xls(c):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Staff')

    ws.write(0, 0, 'Employee', style0)
    ws.write(0, 2, 'Type', style0)
    ws.write(0, 4, 'Academic degree', style0)
    i = 1
    for x in c:
        ws.write(i, 0, x.patronymic)
        ws.write(i, 2, x.typestr)
        ws.write(i, 4, x.academic_degreestr)
        i += 1
    wb.save('scientificWork/static/Staff.xls')


def print_peport_publications_docx(c):
    document = Document()
    document.add_heading('Publications')
    for x in c:
        str = ''
        str += x.bookName
        str += ' ( '
        str += x.user.patronymic
        str += ' )'
        document.add_paragraph(str)
    document.save("scientificWork/static/Publications.docx")


def print_peport_staff_docx(c):
    document = Document()
    document.add_heading('Staff')
    for x in c:
        str = ''
        str += x.patronymic
        str += ' ( '
        str += x.typestr
        str += ', '
        str += x.academic_degreestr
        str += ' )'
        document.add_paragraph(str)
    document.save("scientificWork/static/Staff.docx")
