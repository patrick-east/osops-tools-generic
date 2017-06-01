#!/usr/bin/env python

import shade

shade.simple_logging(debug=True)
c = shade.openstack_cloud()

vms = c.list_servers(all_projects=True)
ports = c.list_ports()

known_ips = set()

for vm in vms:
    if vm.status == 'ACTIVE':
        for net, ips in vm.networks.iteritems():
            for ip in ips:
                known_ips.add(ip)

print "known ip addresses of ACTIVE VM's: " + str(known_ips)

for port in ports:
    for fixed_ip in port['fixed_ips']:
        ip = fixed_ip['ip_address']
        if ip in known_ips:
            print 'Ignoring known ip: ' + str(ip)
        else:
            print 'Deleting port %s with ip %s' % (port['id'], ip)
            c.delete_port(port['id'])
        break
