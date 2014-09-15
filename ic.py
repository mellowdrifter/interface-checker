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

device=[]
if len(sys.argv) < 2:
    print"""
This app requires an argument
example: ic.py hostname
"""
    exit()
else:
    device = sys.argv[1]
community="public"
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

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
            else:
                for varBindTableRow in varBindTable: #varBindTableRow is each interface and oid number. Table is all together
                    for name, val in varBindTableRow:
                        int_name.append(name.prettyPrint())
                        int_oid.append(val.prettyPrint())
                        
        return int_name, int_oid

    except:
        return None

if __name__ == "__main__":
    name,oid=interface_list(device)
    for i in range(len(name)):
        print name[i],"=",oid[i]
