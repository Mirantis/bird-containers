# kargo-multirack
This is addon, which can extend k8s env to multirack case (Route Redistribution container will be used).

Ansible inventory for kargo should looks like:

```
[all]
node1    ansible_host=10.90.1.2 ip=10.90.1.2
node2    ansible_host=10.90.1.3 ip=10.90.1.3
node3    ansible_host=10.90.2.4 ip=10.90.2.4

[all:vars]
calico_network_backend="none"

.....

[rack1]
node1
node2

[rack1:vars]
  as_number=65001
  subnet=10.90.1.0/24
  tor=10.90.1.254
  bgpport=179
  rr_bgpport=180
  rack_no=1

[rack2]
node3

[rack2:vars]
  as_number=65002
  subnet=10.90.2.0/24
  tor=10.90.2.254
  bgpport=179
  rr_bgpport=190
  rack_no=2
```

