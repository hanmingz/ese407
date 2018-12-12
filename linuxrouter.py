from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

class LinuxRouter( Node ):
	"A Node with IP forwarding enabled."

	def config(self, **params):
		super(LinuxRouter, self).config(**params)
		self.cmd('sysctl net.ipv4.ip_forward=1')

	def terminate(self):
		self.cmd('sysctl net.ipv4.ip_forward=0')
		super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
	def build(self, **opts):
		
		defaultIP = '10.0.1.1/24' #IP address for r0-eth1
		r0 = self.addNode('r0', cls=LinuxRouter, ip=defaultIP)
		r1 = self.addNode('r1', cls=LinuxRouter, ip = '10.0.2.1/24')


		h01=self.addHost('h01', ip = '10.0.1.2/24', defaultRoute='via 10.0.1.1')
		h02=self.addHost('h02', ip = '10.0.1.3/24', defaultRoute='via 10.0.1.1')

		h11 = self.addHost('h11', ip = '10.0.2.2', defaultRoute='via 10.0.2.1')
 		
		s0 = self.addSwitch('s0')

		self.addLink(h01, s0)
		self.addLink(h02, s0)
		self.addLink(r0, s0, intfName1='r0-eth1', params1={'ip':'10.0.1.1/24'})

		self.addLink(r1, r0, intfName1='r1-eth1', intfName2='r0-eth2', params1 = {'ip':'10.1.1.2/24'}, params2={'ip':'10.1.1.1/24'})
		self.addLink(h11, r1, intfName2='r1-eth2', params2={'ip':'10.0.2.1/24'})


def run():
	topo = NetworkTopo()
	net = Mininet(topo=topo)
	net.start()
	net['r0'].cmd('route add -net 10.0.2.0 netmask 255.255.255.0 r0-eth2')
	net['r0'].cmd('route add -net 10.0.1.0 netmask 255.255.255.0 r0-eth1')
	net['r0'].cmd('route add -net 10.1.1.0 netmask 255.255.255.0 r0-eth2')
	net['r1'].cmd('route add -net 10.0.1.0 netmask 255.255.255.0 r1-eth1')
	net['r1'].cmd('route add -net 10.0.2.0 netmask 255.255.255.0 r1-eth2')
	net['r1'].cmd('route add -net 10.1.1.0 netmask 255.255.255.0 r1-eth1')

	CLI(net)
	net.stop()

if __name__=='__main__':
	setLogLevel('info')
	run()

