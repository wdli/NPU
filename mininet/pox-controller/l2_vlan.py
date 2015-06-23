"""
An L2 switch capable of vlan
create: May 15, 2015
        WORK-IN_PROGRESS!!!
Usage: 
   1. Launch a mininet
   2. Launch this controller: pox log.level --DEBUG l2_vlan

"""


from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
#from pox.lib.util import EthAddr

import time

#
# Set up the logger
#
log = core.getLogger()

#
# class L2VlanSwtich
#
class L2VlanSwtich(object):
    def __init__(self, connection):
        log.info("*** L2VlanSwtich init")
        self._connection_ = connection
	

    
#
# Class l2_vlan
#
#
class l2_vlan(object):
    def __init__(self):
        log.info("*** To add myself as a listener to connection up event! ")
	core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        #import pdb; pdb.set_trace()	
        log.info("*** Connection up event: %s" % (event.connection))
	L2VlanSwtich(event.connection)


#
# launch function
#
def launch (vlan_id = 0):
    print "*** vlan id: ", vlan_id
    core.registerNew(l2_vlan)
    
