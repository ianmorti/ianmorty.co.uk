Title: Auditing VMWare hosts with pysphere
Author: Ian Mortimer
Date: 2015-01-18
Tags: vmware, python, sysadmin
Category: Development

So you have a bunch of hosts in a datacenter and you want to find out what hosts are running on each one.  Well, you could fire up the vsphere client but, wait, you're on a mac or linux box and the web client is flash based and sucks.  Well, let's do this programatically then using [pysphere](https://code.google.com/p/pysphere/).

First, fire up the interactive shell and connect to vcenter:

	import pysphere
    vis = pysphere.VIServer()
    vis.connect("myhost.mycompany,com", "myuser", "mypassword")

From this point, the `vis` object gives you full access to most things in vcenter.  Let's get a list of all the datacenters you have:

	vis.get_datacenters()
	
	# example ouput
	{'datacenter-2': 'NO_RD',
 	 'datacenter-7': 'UK_R&D',
 	 'datacenter-741': 'NO_BLIX_MNS',
 	 'datacenter-965': 'US_MNS'}
	
This returns a dictionary containing the datacenter name (as vmware sees it) and the friendly name that you see in vCentre.
Cool, so now let's take the datacenter you're interested in and see the hosts associated with it:

	hosts = vis.get_hosts(from_mor=("datacenter-7", pysphere.MORTypes.Datacenter))
	
Here, we're using the `get_hosts()` method and filtering out stuff using a particular MOR (Managed Object Reference).  This will return us all hosts for `datacenter-7` as a dictionary containing the internal vcenter name and the friendly name of each host.
Now you can do things with this dictionay of hosts like getting all the VM's that are running on each one:

	for host, name in hosts.iteritems():
        stuff[name] = vis.get_registered_vms(advanced_filters={"runtime.host": host})
    
`stuff` is now a dictionary keyed on host name with a list of all VM's on that host.  
Hang on, we said get a list of VM's _running_ on that host, well, let's just add another filter then:.

    for host,name in hosts.iteritems():
        onstuff[name] = vis.get_registered_vms(advanced_filters={"runtime.host": host, "runtime.powerState":"poweredOn"})
        
From here you could do things like printing them out to show someone:

    for host, vms in onstuff.iteritems():
    print "Host {} ({}):".format(host, len(vms)
    for vm in vms:
        print " - {}".format(vm)

