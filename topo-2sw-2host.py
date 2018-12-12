from mininet.topo import Topo

class MyTopo(Topo):
	"Simple Topology Example"
	
	def __init__(self):
		"create custom Topo"
	
		Topo.__init__(self)

		leftHost = self.addHost('h1')
		rightHost = self.addHost('h2')
		rightrightHost = self.addHost('h3')
		leftSwitch = self.addSwitch('s3')
		rightSwitch = self.addSwitch('s4')
	
		self.addLink(leftHost, leftSwitch)
		self.addLink(leftSwitch, rightSwitch)
		self.addLink(rightSwitch, rightHost)
		self.addLink(rightrightHost, rightSwitch)

topos = {'mytopo':(lambda: MyTopo() ) }
