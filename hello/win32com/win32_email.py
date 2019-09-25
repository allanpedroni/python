import win32com.client as win32

outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")

# https://stackoverflow.com/questions/22813814/clearly-documented-reading-of-emails-functionality-with-python-win32com-outlook
# https://docs.microsoft.com/en-us/dotnet/api/microsoft.office.interop.outlook.mailitem?redirectedfrom=MSDN&view=outlook-pia#properties_
# https://www.google.com/search?q=win32com.client.Dispatch(%22Outlook.Application%22)&rlz=1C1SQJL_enBR856BR856&oq=win32com.client.Dispatch(%22Outlook.Application%22)&aqs=chrome..69i57.856j0j7&sourceid=chrome&ie=UTF-8
# https://pbpython.com/windows-com.html

# for i in range(50):
try:
    box = outlook.GetDefaultFolder(6)  # caixa de Entrada

    for email in box.Items:
        print('Subject:', email.Subject)
        print('To:', email.To)
        print('From:', email.SenderName)
        # print('Body:', email.Body)
        print('------')

    # print(i,len(box.Items))

    name = box.Name
    print(6, name)
except:
    pass
