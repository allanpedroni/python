import win32com.client
import time
shell = win32com.client.Dispatch("WScript.Shell")
#shell.Run("outlook")
shell.Run("chrome www.uol.com.br")
shell.AppActivate("Outlook")
shell.AppActivate("Chrome")
shell.SendKeys("{TAB}", 0) # 1 für Pause = true 0 für nein
time.sleep(0.03)
shell.SendKeys("{TAB}", 0)
time.sleep(0.03)
shell.SendKeys("{TAB}", 0)
time.sleep(0.03)
shell.SendKeys("{TAB}", 0)