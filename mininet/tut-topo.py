#!/usr/bin/env python3
# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
############################################################################
# RDS-TUT jfpereira - Read all comments from this point on !!!!!!
############################################################################
# This code is given in 
# https://github.com/p4lang/behavioral-model/blob/main/mininet/1sw_demo.py
# with minor adjustments to satisfy the requirements of RDS-TP3. 
# This script works for a topology with one P4Switch connected to 253 P4Hosts. 
# In this TP3, we only need 1 P4Switch and 2 P4Hosts.
# The P4Hosts are regular mininet Hosts with IPv6 suppression.
# The P4Switch it's a very different piece of software from other switches 
# in mininet like OVSSwitch, OVSKernelSwitch, UserSwitch, etc.
# You can see the definition of P4Host and P4Switch in p4_mininet.py
###########################################################################

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSSwitch

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep

# If you look at this parser, it can identify 4 arguments
# --behavioral-exe, with the default value 'simple_switch'
## this indicates that the arch of our software switch is the 'simple_switch'
## and any p4 program made for this arch needs to be compiled against de 'v1model.p4'
# --thrift-port, with the default value of 9090, which is the default server port of
## a thrift server - the P4Switch instantiates a Thrift server that allows us
## to communicate our P4Switch (software switch) at runtime
# --num-hosts, with default value 2 indicates the number of hosts...
# --json, is the path to JSON config file - the output of your p4 program compilation
## this is the only argument that you will need to pass in orther to run the script
parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", default='simple_switch')
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--num-hosts', help='Number of hosts to connect to switch',
                    type=int, action="store", default=2)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)

args = parser.parse_args()

class Triangle(Topo):

    def __init__(self, sw_path, json_path, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # adding P4Switches (Routers)
        router1 = self.addSwitch('R1',
                                cls = P4Switch,
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = 9090
                                )
        
        router2 = self.addSwitch('R2',
                                sw_path = sw_path,
                                cls = P4Switch,
                                json_path = json_path,
                                thrift_port = 9091
                                )
        
        router3 = self.addSwitch('R3',
                                cls = P4Switch, 
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = 9092
                                )
        
        #Add Hosts R1
        host11 = self.addHost('h11',
                                ip = '192.168.1.11/24',
                                mac = '00:00:00:00:01:11')
        
        #host12 = self.addHost('h12',
        #                        ip = '192.168.1.12',
        #                        mac = '00:00:00:00:01:12')
        
        #Server1 = self.addHost('Server1',
        #                        ip = '192.168.1.10',
        #                        mac = '00:00:00:00:01:10')
        
        #Add Hosts R2
        host21 = self.addHost('h21',
                                ip = '192.168.2.21/24',
                                mac = '00:00:00:00:02:21')
        
        #host22 = self.addHost('h22',
        #                        ip = '192.168.2.22',
        #                        mac = '00:00:00:00:02:22')
        
        #Server2 = self.addHost('Server2',
        #                        ip = '192.168.2.20',
        #                        mac = '00:00:00:00:02:20')
        
        #Add Hosts R3
        host31 = self.addHost('h31',
                                ip = '192.168.3.31/24',
                                mac = '00:00:00:00:03:31')
        
        #host32 = self.addHost('h32',
        #                        ip = '192.168.3.32',
        #                        mac = '00:00:00:00:03:32')
        
        #Server3 = self.addHost('Server3',
        #                        ip = '192.168.3.30',
        #                        mac = '00:00:00:00:03:30')
        
        #Add Links Inner
        self.addLink(router1, router2, port1 = 2, port2 = 2, addr1 = '00:01:02:00:00:00', addr2 = '00:02:01:00:00:00')
        self.addLink(router2, router3, port1 = 3, port2 = 3, addr1 = '00:02:03:00:00:00', addr2 = '00:03:02:00:00:00')
        self.addLink(router3, router1, port1 = 2, port2 = 3, addr1 = '00:03:01:00:00:00', addr2 = '00:01:03:00:00:00')

        #Add Links R1
        self.addLink(router1, host11, port1 = 1, port2 = 1, addr1 = '00:01:00:00:00:00')
        #self.addLink(router1, host12, port1 = 1, port2 = 1, addr1 = '00:01:00:00:00:00')
        #self.addLink(router1, Server1, port1 = 1, port2 = 1, addr1 = '00:01:00:00:00:00')

        #Add Links R2
        self.addLink(router2, host21, port1 = 1, port2 = 1, addr1 = '00:02:00:00:00:00')
        #self.addLink(router2, host22, port1 = 1, port2 = 1, addr1='00:02:00:00:00:00')
        #self.addLink(router2, Server2, port1 = 1, port2 = 1, addr1='00:02:00:00:00:00')

        #Add Links R3 (Needs Confirm - Wrote from Mem)
        self.addLink(router3, host31, port1 = 1, port2 = 1, addr1='00:03:00:00:00:00')
        #self.addLink(router3, host32, port1 = 1, port2 = 1, addr1='00:03:00:00:00:00')
        #self.addLink(router3, Server3, port1 = 1, port2 = 1, addr1='00:03:00:00:00:00')
        

def main():
    num_hosts = args.num_hosts

    #topo = SingleSwitchTopo(args.behavioral_exe,args.json,args.thrift_port,num_hosts)
    topo = Triangle(args.behavioral_exe,args.json)

    # the host class is the P4Host
    # the switch class is the P4Switch
    net = Mininet(topo = topo,
                  host = P4Host,
                  controller = None)

    # Here, the mininet will use the constructor (__init__()) of the P4Switch class, 
    # with the arguments passed to the SingleSwitchTopo class in order to create 
    # our software switch.
    net.start()

    # an array of the mac addrs from the switch
    # sw_mac = [sw_mac_base % (n + 1) for n in range(num_hosts)]
    sw_mac = ['00:01:00:00:00:00','00:02:00:00:00:00','00:03:00:00:00:00']

    # an array of the ip addrs from the switch 
    # they are only used to define defaultRoutes on hosts 
    # sw_addr = [sw_ip_base % (n + 1) for n in range(num_hosts)]
    sw_addr = ['192.168.1.254','192.168.2.254','192.168.3.254']

    # h.setARP() populates the arp table of the host
    # h.setDefaultRoute() sets the defaultRoute for the host
    # populating the arp table of the host with the switch ip and switch mac
    # avoids the need for arp request from the host

    for n in range(len(sw_addr)):

        h = net.get('h%d1' % (n+1))
        h.setARP(sw_addr[n], sw_mac[n])
        h.setDefaultRoute("dev eth0 via %s" % sw_addr[n])

        #h = net.get('h%d2' % (n+1))
        #h.setARP(sw_addr[n], sw_mac[n])
        #h.setDefaultRoute("dev eth0 via %s" % sw_addr[n])
#
        #h = net.get('Server%d' % (n+1))
        #h.setARP(sw_addr[n], sw_mac[n])
        #h.setDefaultRoute("dev eth0 via %s" % sw_addr[n])

    hosts = ['h11','h21','h31']
    #hosts = ['h11','h12','Server1','h21','h22','Server2','h31','h32','Server3']
    for host in hosts:
        h = net.get(host)
        h.describe()


    sleep(1)  # time for the host and switch confs to take effect

    print("Ready !")

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
