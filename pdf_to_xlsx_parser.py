import pandas as pd
import tabula

pdf_path = r"C:\Users\CND367\Documents\Python Scripts\WR_WebScraper\Water_Right_WebScraper\pdfs\PRMS_tables_5.2.1.pdf"
excel_path = r"C:\Users\CND367\Documents\Python Scripts\WR_WebScraper\Water_Right_WebScraper\pdfs\params_table.csv"


tabula.convert_into(pdf_path, excel_path, pages='19-42', output_format='csv')

