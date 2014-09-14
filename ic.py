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


interface = []
def interface_list(x):
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget(('172.16.64.50', 161)),
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
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                    interface.append[val.prettyPrint()]
    return interface

