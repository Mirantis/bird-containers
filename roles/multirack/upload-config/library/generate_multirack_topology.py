#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import *
import json

DOCUMENTATION = """
---
module: generate_multirack_topology
short_description: Generate multirack_topology hash which can be uploaded into etcd
description:
  - Generate multirack_topology hash from inventory. Result can be uploaded into etcd
version_added: "2.0"
options:
  inventory:
    required: true
    default: null
    description:
      - 'hostvars' should be here
author: "Sergey Vasilenko (svasilenko@mirantis.com)"
"""

EXAMPLES = """
- name: Generate multirack_topology
  generate_multirack_topology: inventory="{% for host in groups['all'] %}{{ hostvars[host]|to_json }}{% endfor %}"
"""

# RETURN = """
# """

def main():
    module = AnsibleModule(
        argument_spec = dict(inventory = dict(required=True))
    )
    # this is a workaround to https://github.com/ansible/ansible/issues/13838
    inventory = "[" + module.params.get("inventory").replace("}{","},{") + "]"
    nodes = json.loads(inventory)
    racks = {}
    for node in nodes:
        rack_no = int(node.get('rack_no', 0))
        if 0 == rack_no:
            continue
        rack_no_name = "{0}".format(rack_no)
        if racks.get(rack_no_name, None) == None:
            # we can setup rack by first node, because group-based variables are equal for all nodes into rack
            racks[rack_no_name] = {
              'RRs': [],
              'RR-clients': [],
              'rack_no': rack_no,
              'as_number': node.get('as_number', 65000+rack_no),
              'subnet': node.get('subnet', "10.222.{0}.0/24".format(rack_no)),
              'tor': node.get('tor', "10.222.{0}.254".format(rack_no)),
              'bgpport': int(node.get('bgpport', 179)),
              'rr_bgpport': int(node.get('rr_bgpport', int(node.get('bgpport', 179)) + 1))
            }
        racks[rack_no_name]['RR-clients'].append({
          'ipaddr': node.get('ip'),
          'bgpport': int(node.get('bgpport', 179)),
          'nexthop': node.get('nexthop', 'keep')
        })
        if 'bird-rr' in node.get('group_names', []):
            # RR should be run on kube_master
            racks[rack_no_name]['RRs'].append({
              'ipaddr': node.get('ip'),
              'bgpport': racks[rack_no_name]['rr_bgpport'],
              'nexthop': node.get('nexthop', 'keep')
            })
    for rack in racks:
        # remove temporary saved values
        del(racks[rack]['rr_bgpport'])
    res = {
      'racks': racks,
    }
    module.exit_json(**res)

if __name__ == '__main__':
        main()