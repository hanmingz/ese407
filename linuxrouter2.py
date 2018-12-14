from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel, info

N = 2

class LinuxRouter( Node ):
	"A Node with IP forwarding enabled."

	def config(self, **params):
		super(LinuxRouter, self).config(**params)
		self.cmd('sysctl net.ipv4.ip_forward=1')

	def terminate(self):
		self.cmd('sysctl net.ipv4.ip_forward=0')
		super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
	def __init__(self):
		super(NetworkTopo, self).__init__()
		h1 = self.addHost('h1', ip = ip(0, 10, 24), defaultRoute = 'via '+ip(0, 2))
		h2 = self.addHost('h2', ip = ip(2, 10, 24), defaultRoute = 'via '+ip(2, 1))
		rlist = []

		for i in range(1,N+1):
			ri = self.addHost('r'+str(i), cls=LinuxRouter)
			rlist.append(ri)

		self.addLink( h1, rlist[0], intfName1 = 'h1-eth0', intfName2 = 'r1-eth0')

		for i in range(1,N):  # link from ri to r[i+1]
			self.addLink(rlist[i-1], rlist[i], inftname1 = 'r'+str(i)+'-eth1', inftname2 = 'r'+str(i+1)+'-eth0')
 
		self.addLink( rlist[N-1], h2, intfName1 = 'r'+str(N)+'-eth1', intfName2 = 'h2-eth0')




def run():
	topo = NetworkTopo()
	net = Mininet(topo=topo, link = TCLink, autoSetMacs = True)
	net.start()
	for i in range(1, N+1):
		r = net['r'+str(i)]
		left_intf  = 'r'+str(i)+'-eth0'
		right_intf = 'r'+str(i)+'-eth1'
		r.cmd('ifconfig ' + left_intf + ' ' + ip(i-1, 2, 24))
		r.cmd('ifconfig ' + right_intf + ' ' +ip(i,   1, 24))
		rp_disable(r)

	h1 = net['h1']
	h2 = net['h2']
	h1.cmd('/usr/sbin/sshd')
	h2.cmd('/usr/sbin/sshd')
	for i in range(1, N+1):
		r = net['r'+str(i)]
		r.cmd('/usr/sbin/sshd')

	for i in range(1,N):
		r = net['r'+str(i)]
		right_intf = 'r' + str(i) + '-eth1'
		r.cmd('ip route add to ' + ip(N,0,24) + ' via ' + ip(i,2) + ' dev ' + right_intf)

	for i in range(2,N+1):
		r = net['r'+str(i)]
		left_intf = 'r' + str(i) + '-eth0'
		r.cmd('ip route add to ' + ip(0,0,24) + ' via ' + ip(i-1,1) + ' dev ' + left_intf)

	CLI(net)
	net.stop()


# The following generates IP addresses from a subnet number and a host number
# ip(4,2) returns 10.0.4.2, and ip(4,2,24) returns 10.0.4.2/24
def ip(subnet,host,prefix=None):
	addr = '10.0.'+str(subnet)+'.' + str(host)
	if prefix != None: addr = addr + '/' + str(prefix)
	return addr


# For some examples we need to disable the default blocking of forwarding of packets with no reverse path
def rp_disable(host):
	ifaces = host.cmd('ls /proc/sys/net/ipv4/conf')
	ifacelist = ifaces.split()    # default is to split on whitespace
	for iface in ifacelist:
		if iface != 'lo': host.cmd('sysctl net.ipv4.conf.' + iface + '.rp_filter=0')


if __name__=='__main__':
	setLogLevel('info')
	run()


