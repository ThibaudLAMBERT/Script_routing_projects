import json

def create_router(name, protocol, as_number, router_id, interfaces):
    return {
        "name": name,
        "protocol": protocol,
        "as": as_number,
        "id": router_id,
        "interfaces": interfaces
    }

def create_interface(name, ip, neighbor):
    return {
        "name": name,
        "ip": ip,
        "neighbor": neighbor
    }

routers = [
    create_router("RR1", "RIP", "111", "1.1.1.1", [
        create_interface("g1/0", "2001:111:1:1::2", "RR2"),
        create_interface("g2/0", "2001:111:1:2::2", "RR3")
    ]),
    create_router("RR2", "RIP", "111", "1.1.1.2", [
        create_interface("g1/0", "2001:111:1:1::1", "RR1"),
        create_interface("f0/0", "2001:100:1::1", "RO2")
    ]),
    create_router("RR3", "RIP", "111", "1.1.1.3", [
        create_interface("g1/0", "2001:111:1:2::1", "RR1"),
        create_interface("f0/0", "2001:100:2::1", "RO3")
    ]),
    create_router("RO2", "OSPF", "112", "1.1.2.2", [
        create_interface("g1/0", "2001:112:1:1::1", "RO1"),
        create_interface("f0/0", "2001:100:1::2", "RR2")
    ]),
    create_router("RO1", "OSPF", "112", "1.1.2.1", [
        create_interface("g1/0", "2001:112:1:1::2", "RO2"),
        create_interface("g2/0", "2001:112:1:2::2", "RO3")
    ]),
    create_router("RO3", "OSPF", "112", "1.1.2.3", [
        create_interface("g1/0", "2001:112:1:2::1", "RO1"),
        create_interface("f0/0", "2001:100:2::2", "RR2")
    ])
]

json_data = {"data": routers}

with open("network_topology.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print("JSON file created: network.json")
