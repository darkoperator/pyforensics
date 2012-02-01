__author__="Carlos Perez carlos_perez@darkoperator.com"
__date__ ="$Sep 11, 2010 8:35:52 AM$"

import getopt
import sys
import wmi


def usage():
    """
    Function for presenting usage of the tool.
    """
    print "Proclist by Carlos Perez carlos_perez@darkoperator.com"
    print "Tool for printing to STDOUT a list of processes running on a local"
    print "or remote computer and their details using WMI.\n"
    print "proclist.exe <OPTIONS>"
    print "\t-h\tRemote Host to connect to."
    print "\t-u\tUsername for Connection to Remote Host"
    print "\t-p\tPassword for Connection to Remote Host"
    print "\t-l\tPresent output in a list format to STDOUT."
    print "\t-c\tPresent output in a CSV format to STDOUT."
    sys.exit(0)


def wmi_date_format(dtmDate):
    """
    This function is for formatting the time returned by WMI in a more comprehensible format
    """
    strDateTime = ""
    if (dtmDate[4] == 0):
        strDateTime = dtmDate[5] + '/'
    else:
        strDateTime = dtmDate[4] + dtmDate[5] + '/'
    if (dtmDate[6] == 0):
        strDateTime = strDateTime + dtmDate[7] + '/'
    else:
        strDateTime = strDateTime + dtmDate[6] + dtmDate[7] + '/'
        strDateTime = strDateTime + dtmDate[0] + dtmDate[1] + dtmDate[2] + dtmDate[3] + " " + dtmDate[8] + dtmDate[9] + ":" + dtmDate[10] + dtmDate[11] +':' + dtmDate[12] + dtmDate[13]
    return strDateTime


def process_list_csv(out_type, c):

    # Set first line with field name in case output is CSV
    if out_type == 1:
        print "Name,Caption,Commad Line,Creation Date,Parent PID,PID,Owner"

    # Get data for each process
    for process in c.Win32_Process ():

        # Initialize variable for data per process
        name = ""
        command_line = ""
        date = ""
        ppid = ""
        pid = ""
        owner_name = ""
        caption = ""

        # Retrive data
        if process.Name != None:
            name = process.Name
        if process.Caption != None:
            caption = process.Caption
        if process.CommandLine != None:
            command_line = process.CommandLine
        if process.CreationDate != None:
            date = wmi_date_format(process.CreationDate)
        if process.ParentProcessId != None:
            ppid = process.ParentProcessId
        if process.ProcessId != None:
            pid = process.ProcessId

        # Check for Ownwer, this is not available in 2000 and may error in
        # modern versions of Windows.
        try:
            owner = process.GetOwner()
            if owner[0] != None:
                owner_name = owner[0] + "\\" + owner[2]
        except:
            pass

        # Print general output
        if out_type == 0:
            print "Name: ",name
            print "Caption: ", caption
            print "Command Line: ", command_line
            print "Creation Date: ", date
            print "Parent PID: ", ppid
            print "PID: ", pid
            print "Owner: "+ owner_name
            print ""

        # Print CSV formated output
        if out_type == 1:
            print name + "," + caption + ",\"" + command_line + "\"," + date + "," + str(ppid) + "," + str(pid) + "," + owner_name


def main():

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

    if len(sys.argv) > 1:
        process_list_csv(out_type,c)
    else:
        usage()
if __name__ == '__main__':
    main()