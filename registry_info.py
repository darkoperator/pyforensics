import win32api
import win32con
import getopt
import sys
import re
import string

def get_key_time(regkey,recur):
    """
    Function for getting the last write time of a given registry key.
    """

    # Split the registry key into hive name and path
    hive,path = string.split(regkey,"\\",1)

    # Select proper hive
    if re.search(r"(HKLM|HKEY_LOCAL_MACHINE)",hive):
        key = win32con.HKEY_LOCAL_MACHINE

    elif re.search(r"(HKCU|HKEY_CURRENT_USER)",hive):
        key = win32con.HKEY_CURRENT_USER

    elif re.search(r"(HKU|HKEY_USERS)",hive):
        key = win32con.HKEY_USERS

    elif re.search(r"(HKCC|HKEY_CURRENT_CONFIG )",hive):
        key = win32con.HKEY_CURRENT_CONFIG

    elif re.search(r"(HKCR|HKEY_CLASSES_ROOT)",hive):
        key = win32con.HKEY_CLASSES_ROOT

    # Get the last write for the key, error if not possible

    try:
        access = win32con.KEY_READ | win32con.KEY_ENUMERATE_SUB_KEYS | win32con.KEY_QUERY_VALUE
        hkey = win32api.RegOpenKey(key, path, 0, access)
        num = win32api.RegQueryInfoKeyW(hkey)

    except Exception, e:
        print "could not open Key", hive + "\\" + path, e[2]
        sys.exit(1)

    if recur:
        for n in xrange(num["SubKeys"]):
            try:
                eKey = win32api.RegEnumKey(hkey,n)
                hKey = win32api.RegOpenKey(key, path+"\\"+eKey, 0, access)
                mod_time = win32api.RegQueryInfoKeyW(hKey)["LastWriteTime"]
                print '"' + hive + "\\" + path + "\\" + eKey + '",', '"' + str(mod_time) + '"'
            except:
                 print '"' + hive + "\\" + path + "\\"+eKey + '",', "\"Access Denied\""

    else:
        print '"' + hive + "\\" + path + '",', '"' + str(num["LastWriteTime"]) + '"'

def usage():
    """
    Function for presenting usage of the tool.
    """
    print "key_time by Carlos Perez carlos_perez@darkoperator.com"
    print "Tool for printing to STDOUT the last write time for a given key.\n"
    print "key_time.exe <OPTIONS>"
    print "\t-r\tRecursively get the last write date for the keys under the given key."
    print "\t-k\tRegistry key to get last write time"

    sys.exit(0)

def main():
    # Set Variables for Options
    recursive = None
    key = None

    # Set Options
    options, remainder = getopt.getopt(sys.argv[1:], 'rk:h')

    # Parse Options
    for opt, arg in options:
        if opt in ('-r'):
            recursive = True
        elif opt in ('-k'):
            key = arg
        elif opt in ('-h'):
            usage()
    get_key_time(key,recursive)

if __name__ == '__main__':
    main()