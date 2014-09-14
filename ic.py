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

import pysnmp
