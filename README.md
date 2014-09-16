#interface-checker
###Backend to check device for :
<ol>
<li>Interface list</li>
<li>Administrative status</li>
<li>Operational status</li>
</ol>

###Requirements:
<ol>
<li>Python2</li>
<li>pysnmp</li>
<li>PrettyTable</li>
</ol>


###Example usage:
>Darren-MBP:interface-checker darren$ ./1.py router-name  
>+-------------------------+-----------------+--------------+--------------------+  
>|        OID Value        |  Interface Name | Admin Status | Operational Status |  
>+-------------------------+-----------------+--------------+--------------------+  
>|  1.3.6.1.2.1.2.2.1.2.1  |       fxp0      |     DOWN     |        DOWN        |  
>|  1.3.6.1.2.1.2.2.1.2.2  |       fxp1      |      UP      |         UP         |  
>| 1.3.6.1.2.1.2.2.1.2.521 |    ge-1/3/0.0   |      UP      |         UP         |  
>+-------------------------+-----------------+--------------+--------------------+  
