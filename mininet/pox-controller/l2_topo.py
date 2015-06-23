#!/usr/bin/python
#
# A sample topology created by using
# mininet's APIs
#
# This is the same as by using CLI
# sudo mn --topo=single,3
# 
# To run with this topology
# sudo mn --custom ./l2_topo.py --topo mytopo
#

from mininet.topo import Topo


class MyTopo(Topo):

    def __init__(self):
       Topo.__init__(self)

       # add hosts
       h1 = self.addHost("myh1")
       h2 = self.addHost("myh2")
       h3 = self.addHost("myh3")

       # add a switch
       sw1 = self.addSwitch("mysw1")
        
       # add links
       self.addLink(h1,sw1)
       self.addLink(h2,sw1)
       self.addLink(h3,sw1)


topos = { 'mytopo': (lambda: MyTopo())}

       
       
       


