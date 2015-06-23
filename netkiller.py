def main():

    if not tryImports():
        exit(1)
    args = parseArgs()

    try:
        deviceList = listProcesses(getNetworkDevices())
        deviceList= trimList(args.devices,deviceList)
        
        if args.dash_nine and args.kill:
            print "error, you can't kill something twice..."
            exit(2)
        
        if args.dash_nine:
            killdashnine(deviceList)
        elif args.kill:
            kill(deviceList)
    except KeyError,e:
        print e
        print "well shit, there's a key error, make a bug report"
        exit(1)
    finally:
        print("you murderer....")
        exit(0)
def trimList(inDevices, deviceList):
    if inDevices is '*':
        return deviceList
    else:
        temp = []
        x = len(deviceList)
        devices = str(inDevices).split(',')

        for i in deviceList:
            if i[1] in devices:
                temp.append(i)
        return temp


def killdashnine(processes):
    import psutil
    for i in processes:
        kill_proc_tree(i[0], True)
    return

def kill(processes):
    import psutil
    for i in processes:
        psutil.Process(i[0]).kill
    return

def kill_proc_tree(pid, including_parent=True):
    import psutil
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)

# This method will parse the command line args and will return 2
# if the proper arguments are not there
#
# -d <Device Name(s)>
# This flag will take device names separated by commas with NO spaces
# to use in the kill method specified in other args
# ex. <prog> -d eth0,wlan0
#
# if the parameter is '*', the program will use ALL devices found by
# getNetworkDevices()
#
# -k
# the equivalent of the bash command kill PID
#
# -9
# the equivalent of kill -9 PID
#
# TODO: implement option to specify kill method for individual devices
#
#
#####################################################
# ERROR HANDLING FLAGS
#####################################################
#
# TODO: this
#
#

def parseArgs():
    import argparse
    parser = argparse.ArgumentParser('netkiller.py', usage='prog.py -d=<devices> -9/k/l')
    parser.add_argument('-d','--devices', help='Device names to operate on', required=True)
    parser.add_argument('-k','--kill', help='Standard kill, equivalent to \'kill PID\'', required=False, action='store_true')
    parser.add_argument('-9','--dash-nine', help='The equivalent of \'kill -9 PID\'', action='store_true')
    args = parser.parse_args()
    if not args.kill and not args.dash_nine:
        parser.error("You must specify a kill option: -9 or -k\n")
        exit(1)
    return args

# This method checks to see if the proper libraries are available to use
# These include netifaces, optparse
# ------------------------------------------------------------------------
# When the libraries are not found, the method returns false and prints
# an error message, returns true otherwise

def tryImports():
    try:
        import netifaces
    except ImportError:
        print "[-] netifaces not found\nto install:\n\tpip install netifaces"
        return False

    try:
        import argparse
    except ImportError:
        print "[-] argparse not found\nto install:\n\tpip install argparse"
        return False

    try:
        import psutil
    except ImportError:
        print "[-] psutil not found\nto install:\n\tpip install psutil"
        return False
    return True


# This method will return a list of all PID's running on the device or devices
# the device parameter is a list of strings where each string element is the
# name of the device/interface
#
# Precondidtion:
#
# getNetworkDevices() returned a valid non-empty dict containing net device + IP key:value pairs
# where the device is the key and the IP is the value
#
# Ex. {"10.0.0.2":"wlan0", "aa:bb:cc:dd":"eth0"}
#
# Postcondition:
#
# This method will return a list of pairs (of size 2) with the first element
# of the tuple being the PID and the last element of the pair being the
# network interface name
# Ex. [(123,'eth0'),(444,'eth0'),(4343,'wlan0')]
#
# note: unless the PID's are sorted when grabbed, they won't be sorted by this method.

def listProcesses(devices):

    #dear god this is hackish
    devices['0.0.0.0'] = 'lo'
    devices['127.0.1.1'] = 'lo'
    devices['::'] = 'lo'
    devices['::1'] = 'lo'

    import psutil
    la = psutil.net_connections()
    retval = []
    for i in la:
        ####
        #
        # The IP and port are stored as a tuple in the psutil._common.sconn namedtouple at
        # psutil._common.sconn[3] with the IP at [0] and the port at [1]
        #
        # The PID is stored at psutil._common.sconn[6]
        #
        ##
        # print i[3][0] + " " + str(i[3][1])
        # procs.append([i[3][0], str(i[3][1])])
        ####
        if i[6] is not None:
            retval.append((i[6], devices[i[3][0]]))

    # God, I am so sorry. I can feel my Data Structures prof judging me from somewhere
    # ... among other people...
    return list(set(retval))



# This method will grab the device names and return them as a dict
# with each key being the string of the network interface name and the value as the IP
#
# { interface, IP }
#
# Note: WILL RETURN EMPTY LIST if there are no valid devices

def getNetworkDevices():

    import netifaces as ni
    # Something witty about monty python and the holy grail goes here
    import psutil as p

    retval = {}

    if ni.interfaces() is None or ni.interfaces() is ['lo']:
        print "[-] fatal: no network devices found"

    else:
        print "[+] got these devices " + str(ni.interfaces())

    for n in ni.interfaces():
        retval[p.net_if_addrs()[n][0][1]] = n
    return retval


if __name__ == "__main__":
    main()
