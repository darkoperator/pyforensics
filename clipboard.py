#Script file
import win32clipboard
win32clipboard.OpenClipboard()
try:
    cf = win32clipboard.GetClipboardData()
    print cf
except:
    print "Could not get clipboard data"
win32clipboard.CloseClipboard()
