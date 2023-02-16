import pandas as pd


def write_to_excel(df, path):
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, index=True, sheet_name='report')

    # Get access to the workbook and sheet
    workbook = writer.book
    worksheet = writer.sheets['report']

    # Reduce the zoom a little
    worksheet.set_zoom(10)

    (max_row, max_col) = df.shape

    # Add a format. Light red fill with dark red text.
    format = workbook.add_format({'bg_color': '#8b0000'})

    worksheet.conditional_format(0, 0, max_row, max_col, {'type': 'cell', 'criteria': '==', 'value': '1', 'format': format})

    writer.close()
