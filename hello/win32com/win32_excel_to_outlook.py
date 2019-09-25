import win32com.client as win32
import pandas as pd
from pathlib import Path
from datetime import  date

to_email = """
allan.barros@gmail.com; allan.pedroni@oletecnologia.com.br
"""

df = pd.read_csv('https://github.com/chris1610/pbpython/blob/master/data/sample-sales-tax.csv?raw=True')

out_file = Path.cwd() / 'tax_summary.xlsx'

df_summary = df.groupby('category')['ext price', 'Tax amount'].sum()

df_summary.to_excel(out_file)

# Open up an outlook email
outlook = win32.gencache.EnsureDispatch('Outlook.Application')
new_mail = outlook.CreateItem(0)

# Label the subject
new_mail.Subject = "{:%m/%d} Report Update".format(date.today())

# Add the to and cc list
new_mail.To = to_email

# Attach the file
attachment1 = out_file

# The file needs to be a string not a path object
new_mail.Attachments.Add(Source=str(attachment1))

# Display the email
new_mail.Display(True)
# new_mail.Send()
