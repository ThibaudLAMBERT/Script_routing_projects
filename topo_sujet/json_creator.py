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

def create_interface(name, ip, neighbor):
    return {
        "name": name,
        "ip": ip,
        "neighbor": neighbor
    }

routers = [
    create_router("R1", "RIP", "111", "1.1.1.1", [
        create_interface("g1/0", "2001:100:1:2::2", "R2"),
        create_interface("g2/0", "2001:100:1:3::1", "R5")
    ]),
    create_router("R2", "RIP", "111", "1.1.1.2", [
        create_interface("g1/0", "2001:100:1:2::1", "R1"),
        create_interface("g2/0", "2001:100:1:1::1", "R3"),
        create_interface("g3/0", "2001:100:1:4::2", "R5")
    ]),
    create_router("R3", "RIP", "111", "1.1.1.3", [
        create_interface("g1/0", "2001:100:1:1::2", "R2"),
        create_interface("g2/0", "2001:100:1:8::1", "R4"),
        create_interface("g3/0", "2001:100:1:6::1", "R6"),
        create_interface("g4/0", "2001:100:1:7::1", "R7")
    ]),
    create_router("R4", "RIP", "111", "1.1.1.4", [
        create_interface("g1/0", "2001:100:1:8::2", "R3"),
        create_interface("g2/0", "2001:100:1:9::2", "R6"),
        create_interface("f0/0", "2001:100:3:1::1", "R8")
    ]),
    create_router("R5", "RIP", "111", "1.1.1.5", [
        create_interface("g1/0", "2001:100:1:3::2", "R1"),
        create_interface("g2/0", "2001:100:1:5::1", "R6"),
        create_interface("g3/0", "2001:100:1:4::1", "R2")
    ]),
    create_router("R6", "RIP", "111", "1.1.1.6", [
        create_interface("g1/0", "2001:100:1:5::2", "R5"),
        create_interface("g2/0", "2001:100:1:10::2", "R7"),
        create_interface("g3/0", "2001:100:1:6::2", "R3"),
        create_interface("g4/0", "2001:100:1:9::1", "R4")
    ]),
    create_router("R7", "RIP", "111", "1.1.1.7", [
        create_interface("g1/0", "2001:100:1:10::1", "R6"),
        create_interface("g2/0", "2001:100:1:7::2", "R3"),
        create_interface("f0/0", "2001:100:3:3::1", "R14")
    ]),
    create_router("R8", "OSPF", "112", "2.2.2.8", [
        create_interface("g1/0", "2001:100:2:1::1", "R9"),
        create_interface("g2/0", "2001:100:2:3::1", "R13"),
        create_interface("f0/0", "2001:100:3:1::2", "R4")
    ]),
    create_router("R9", "OSPF", "112", "2.2.2.9", [
        create_interface("g1/0", "2001:100:2:1::2", "R8"),
        create_interface("g2/0", "2001:100:2:2::2", "R14"),
        create_interface("g3/0", "2001:100:2:5::2", "R10"),
        create_interface("g4/0", "2001:100:2:4::2", "R13")
    ]),
    create_router("R10", "OSPF", "112", "2.2.1.0", [
        create_interface("g1/0", "2001:100:2:5::1", "R9"),
        create_interface("g2/0", "2001:100:2:8::2", "R12"),
        create_interface("g3/0", "2001:100:2:9::1", "R11"),
    ]),
    create_router("R11", "OSPF", "112", "2.2.1.1", [
        create_interface("g1/0", "2001:100:2:9::2", "R10"),
        create_interface("g2/0", "2001:100:2:10::2", "R12"),
    ]),
    create_router("R12", "OSPF", "112", "2.2.1.2", [
        create_interface("g1/0", "2001:100:2:7::1", "R13"),
        create_interface("g2/0", "2001:100:2:8::1", "R10"),
        create_interface("g3/0", "2001:100:2:10::1", "R11"),
    ]),
    create_router("R13", "OSPF", "112", "2.2.1.3", [
        create_interface("g1/0", "2001:100:2:6::2", "R14"),
        create_interface("g2/0", "2001:100:2:3::2", "R8"),
        create_interface("g3/0", "2001:100:2:7::2", "R12"),
        create_interface("g4/0", "2001:100:2:4::1", "R9")
    ]),
    create_router("R14", "OSPF", "112", "2.2.1.4", [
        create_interface("g1/0", "2001:100:2:6::1", "R13"),
        create_interface("g2/0", "2001:100:2:2::1", "R9"),
        create_interface("f0/0", "2001:100:3:2::2", "R7"),
    ]),
]

json_data = {"data": routers}

with open("network_topology.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print("JSON file created: network.json")
