#!/usr/bin/python

'''Important OIDs:

=== .1.3.6.1.2.1.2.2.1.2 - Interface list ===


=== .1.3.6.1.2.1.2.2.1.7 - Admin Status:
1 : up
2 : down
3 : testing ===


=== .1.3.6.1.2.1.2.2.1.8 - Op status:
1 : up
2 : down
3 : testing
4 : unknown
5 : dormant
6 : notPresent
7 : lowerLayerDown ===
'''

from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import re


device=[]
if len(sys.argv) < 2:
    print"""
This app requires an argument!
example: ic.py hostname
"""
    exit()
else:
    device = sys.argv[1]
community="strawberry"
interface = []

def interface_list(x):
    int_name=[]
    int_oid=[]
    try:
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData(community),
            cmdgen.UdpTransportTarget((x, 161)),
            '1.3.6.1.2.1.2.2.1.2',
        )
        for varBindTableRow in varBindTable: #varBindTableRow is each interface and oid number
            for name, val in varBindTableRow:
                oid_raw=name.prettyPrint()
                oid = re.search(r'1.3.6.1.2.1.2.2.1.2.(\d{0,5})',oid_raw)
                oid = oid.group(1)
                int_oid.append(oid)
                int_name.append(val.prettyPrint())
        return int_oid, int_name
    except:
        return None

def interface_admin(x,y):
    mib_value="1.3.6.1.2.1.2.2.1.7."+y
    admin=[]
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((x, 161)),
        mib_value,
    )
    for name, val in varBinds:
        admin.append(val.prettyPrint())
        if '1' in admin:
            int_admin = 'UP'
        elif '2' in admin:
            int_admin = 'DOWN'
        elif '3' in admin:
            int_admin = 'TESTING'
    return int_admin

def interface_oper(x,y):
    mib_value="1.3.6.1.2.1.2.2.1.8."+y
    oper=[]
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((x, 161)),
        mib_value,
    )
    for name, val in varBinds:
        oper.append(val.prettyPrint())
        if '1' in oper:
            int_oper = 'UP'
        elif '2' in oper:
             int_oper = 'DOWN'
        elif '3' in oper:
             int_oper = 'TESTING'
        elif '4' in oper:
            int_oper = 'UNKNOWN'
        elif '5' in oper:
            int_oper = 'DORMANT'
        elif '6' in oper:
            int_oper = 'NOT-PRESENT'
        elif '7' in oper:
            int_oper = 'LOWER-LAYER-DOWN'
    return int_oper

#def interface_time(x,y):
    mib_value="1.3.6.1.2.1.2.2.1.9."+y
    int_time=[]
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((x, 161)),
        mib_value,
    )
    for name, val in varBinds:
        int_time.append(val.prettyPrint())
    return int_time

if __name__ == "__main__":
    from prettytable import PrettyTable

    print "Checking for interfaces ...",
    oid,name=interface_list(device)
    print "Done"
    toolbar_width = len(name)
    table=PrettyTable(["OID Value","Interface Name","Admin Status","Operational Status"])
    print "Checking "+str(len(name))+" interface values, please wait"
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))
    for i in range(len(name)):
        int_admin = interface_admin(device,oid[i])
        int_oper = interface_oper(device,oid[i])
        #int_time = interface_time(device,oid[i])
        table.add_row(["1.3.6.1.2.1.2.2.1.2."+oid[i],name[i],int_admin,int_oper])
        sys.stdout.write("-")
        sys.stdout.flush()
    print "\n\n"
    print table
