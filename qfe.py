__author__="Carlos Perez carlos_perez@darkoperator.com"

import getopt
import sys
import wmi
import hashlib

# Set Variables for Options
user_name = None
user_password = None
computer = None
out_type = 0

# Set Options
options, remainder = getopt.getopt(sys.argv[1:], 'u:p:h:lc')

# Parse Options
for opt, arg in options:
    if opt in ('-u'):
        user_name = arg
    elif opt in ('-p'):
        user_password = arg
    elif opt in ('-h'):
        computer = arg
    elif opt in ('-c'):
        out_type = 1
# Create Connection depending the values passed
if not user_name:
    c = wmi.WMI ()
else:
    c = wmi.WMI(computer, user=user_name, password=user_password)

def hash_file(file_name,hash_type):
    """
    Compute md5 hash of the specified file
    """

    if hash_type == "md5":
        m = hashlib.md5()

    elif hash_type == "sha1":
        m = hashlib.sha1()

    else:
        print "Hash Type",hash_type,"unknown!"
        sys.exit(1)

    try:
        fd = open(file_name,"rb")
    except IOError:
        print "Unable to open the file in readmode:", file_name
        return
    each_line = fd.readline()
    while each_line:
        m.update(each_line)
        each_line = fd.readline()
    fd.close()
    return m.hexdigest()

def usage():
    """
    Function for presenting usage of the tool.
    """
    print "Proclist by Carlos Perez carlos_perez@darkoperator.com"
    print "Tool for printing to STDOUT MS Updates installed on a local"
    print "or remote computer and their details using WMI.\n"
    print "qfe.exe <OPTIONS>"
    print "\t-h\tRemote Host to connect to."
    print "\t-u\tUsername for Connection to Remote Host"
    print "\t-p\tPassword for Connection to Remote Host"
    print "\t-l\tPresent output in a list format to STDOUT."
    print "\t-c\tPresent output in a CSV format to STDOUT."
    sys.exit(0)
    
def patch_list(out_type):
    """
    Function to list patches installed on given system
    """
    for patch in c.Win32_QuickFixEngineering ():
        print "Host:", patch.Name
        print "ID:", patch.HotFixID
        print "Installed Date:", patch.InstalledOn
        print

file2hash = "e:\osxserverkeys.txt"
print hash_file(file2hash, "md5")
