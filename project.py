""" router topology for ESE407 final project. 
Using rip.py from intronetworks.cs.luc.edu and code referenced resources
from cs.luc.edu.
"""

from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel, info
import os

ENABLE_RIP = True

class LinuxRouter( Node ):	# from the Mininet library
	"A Node with IP forwarding enabled."

	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
		info ('enabling forwarding on ', self)
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()

class MyTopo(Topo):
	def __init__(self, **kwargs):
		super(MyTopo, self).__init__(**kwargs)

		h1 = self.addHost('h1', ip = '124.0.1.2/24', defaultRoute = 'via 124.0.1.1')
		h2 = self.addHost('h2', ip = '124.0.1.3/24', defaultRoute = 'via 124.0.1.1')
		h3 = self.addHost('h3', ip = '124.0.1.4/24', defaultRoute = 'via 124.0.1.1')

		s1 = self.addSwitch('s1')

		r1 = self.addHost('r1', cls = LinuxRouter)

		self.addLink(s1, r1, intfName2 = 'r1-eth0', bw = 5)
		for i in range(1, 4):
			self.addLink('h'+str(i), s1, bw = 5)

		r2 = self.addHost('r2', cls = LinuxRouter)
		r3 = self.addHost('r3', cls = LinuxRouter)
		r4 = self.addHost('r4', cls = LinuxRouter)

		self.addLink(r1, r2, intfName1 = 'r1-eth1', intfName2 = 'r2-eth0', bw = 5)
		self.addLink(r2, r3, intfName1 = 'r2-eth1', intfName2 = 'r3-eth1', bw = 5)
		self.addLink(r3, r4, intfName1 = 'r3-eth2', intfName2 = 'r4-eth2', bw =15)
		self.addLink(r2, r4, intfName1 = 'r2-eth2', intfName2 = 'r4-eth1', bw =15)

		s4 = self.addSwitch('s4')

		h4 = self.addHost('h4', ip = '204.72.30.4/24', defaultRoute = 'via 204.72.30.1')

		h5 = self.addHost('h5', ip = '138.4.0.5/16', defaultRoute = 'via 138.4.0.1')
		h6 = self.addHost('h6', ip = '138.4.0.6/16', defaultRoute = 'via 138.4.0.1')

		self.addLink(h5, s4, bw = 5)
		self.addLink(h6, s4, bw = 5)

		self.addLink(r4, s4, intfName1 = 'r4-eth0', bw = 5)
		self.addLink(r3, h4, intfName1 = 'r3-eth0', bw = 5)


def main():
	os.system("dhclient eth0")
	os.system("sudo wireshark &")
	os.system("apt-get install traceroute")
	myTopo = MyTopo()
	net = Mininet(topo = myTopo, link = TCLink, autoSetMacs = True)
	net.start()

	for i in range(1, 7):
		h = net['h'+str(i)]
		h.cmd('/usr/sbin/sshd')

	for i in range(1, 5):
		r = net['r'+str(i)]
		r.cmd('/usr/sbin/sshd')
		r.cmd('python3 rip.py &')

	net['r1'].cmd('ifconfig r1-eth0 124.0.1.1/24')
	net['r1'].cmd('ifconfig r1-eth1 192.168.0.2/24')
	net['h1'].cmd('python -m SimpleHTTPServer 80 &')

	net['r2'].cmd('ifconfig r2-eth0 192.168.0.1/24')
	net['r2'].cmd('ifconfig r2-eth1 192.168.2.1/24')
	net['r2'].cmd('ifconfig r2-eth2 192.168.1.1/24')

	net['r3'].cmd('ifconfig r3-eth0 204.72.30.1/24')
	net['r3'].cmd('ifconfig r3-eth1 192.168.2.2/24')
	net['r3'].cmd('ifconfig r3-eth2 192.168.3.1/24')

	net['r4'].cmd('ifconfig r4-eth0 138.4.0.1/16')
	net['r4'].cmd('ifconfig r4-eth1 192.168.1.3/24')
	net['r4'].cmd('ifconfig r4-eth2 192.168.3.5/24')

	CLI(net)
	net.stop()

if __name__ == '__main__':
	main()
