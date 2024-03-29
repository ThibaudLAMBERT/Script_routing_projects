import json

def create_router(name, protocol, as_number, router_id, loopback_address, interfaces):
    return {
        "name": name,
        "protocol": protocol,
        "as": as_number,
        "id": router_id,
        "loopback": loopback_address,
        "interfaces": interfaces
    }

def create_interface(name, ip, neighbor, ospf_cost="default", local_pref="None"):
    return {
        "name": name,
        "ip": ip,
        "neighbor": neighbor,
        "ospf_cost": ospf_cost,
        "local_pref" : local_pref
    }


routers = [
    create_router("RR1", "RIP", "111", "1.1.1.1", "2001:111::1/128",  [
        create_interface("g1/0", "2001:111:1:1::2/64", "RR2"),
        create_interface("g2/0", "2001:111:1:2::2/64", "RR3")
    ]),
    create_router("RR2", "RIP", "111", "1.1.1.2", "2001:111::2/128", [
        create_interface("g1/0", "2001:111:1:1::1/64", "RR1"),
        create_interface("f0/0", "2001:100:1::1/64", "RO2")
    ]),
    create_router("RR3", "RIP", "111", "1.1.1.3", "2001:111::3/128", [
        create_interface("g1/0", "2001:111:1:2::1/64", "RR1"),
        create_interface("f0/0", "2001:100:2::1/64", "RO3")
    ]),
    create_router("RO2", "OSPF", "112", "1.1.2.2", "2001:112::2/128", [
        create_interface("g1/0", "2001:112:1:1::1/64", "RO1"),
        create_interface("f0/0", "2001:100:1::2/64", "RR2")
    ]),
    create_router("RO1", "OSPF", "112", "1.1.2.1", "2001:112::1/128", [
        create_interface("g1/0", "2001:112:1:1::2/64", "RO2"),
        create_interface("g2/0", "2001:112:1:2::2/64", "RO3")
    ]),
    create_router("RO3", "OSPF", "112", "1.1.2.3", "2001:112::3/128", [
        create_interface("g1/0", "2001:112:1:2::1/64", "RO1"),
        create_interface("f0/0", "2001:100:2::2/64", "RR2")
    ])
]

json_data = {"data": routers}

with open("Topology/Small/network_topology.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print("JSON file created: network.json")
