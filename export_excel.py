import xlsxwriter
import os

basedir = os.path.abspath(os.path.dirname(__file__))

def export_excel(filename,list_cus):
    # Create a workbook and add a worksheet.
    path_folder = basedir+'/excel'
    if not os.path.exists(path_folder):
            os.mkdir(path_folder)
    workbook = xlsxwriter.Workbook(basedir+'/excel/'+filename+'.xlsx')
    worksheet = workbook.add_worksheet()

    # Some data we want to write to the worksheet.
   
    # Iterate over the data and write it out row by row.
    for row_num, data in enumerate(list_cus):
        worksheet.write_row(row_num, 0, data)

    workbook.close()
    return True