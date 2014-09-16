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
#from tabulate import tabulate
import sys
import re

device=[]
if len(sys.argv) < 2:
    print"""
This app requires an argument
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
    int_admin=[]
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((x, 161)),
        mib_value,
    )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
            print(errorStatus)
    for name, val in varBinds:
        int_admin.append(val.prettyPrint())
        int_admin=str(int_admin)
    return int_admin

def interface_oper(x,y):
    mib_value="1.3.6.1.2.1.2.2.1.8."+y
    int_oper=[]
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((x, 161)),
        mib_value,
    )
    for name, val in varBinds:
        int_oper.append(val.prettyPrint())
        int_oper=str(int_oper)
    return int_oper

if __name__ == "__main__":
    oid,name=interface_list(device)
    for i in range(len(name)):
        int_admin = interface_admin(device,oid[i])
        int_oper = interface_oper(device,oid[i])
        print "1.3.6.1.2.1.2.2.1.2."+oid[i]+"\t\t"+name[i]+"\t\t"+int_admin+"\t\t"+int_oper
