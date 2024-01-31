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

def create_interface(name, ip, neighbor, ospf_cost="default",local_pref="None"):
    return {
        "name": name,
        "ip": ip,
        "neighbor": neighbor,
        "ospf_cost": ospf_cost,
        "local_pref": local_pref
    }

routers = [
    create_router("R1", "RIP", "111", "1.1.1.1", "2001:111::1/128", [
        create_interface("g1/0", "2001:100:1:2::2/64", "R2"),
        create_interface("g2/0", "2001:100:1:3::1/64", "R5")
    ]),
    create_router("R2", "RIP", "111", "1.1.1.2", "2001:111::2/128",[
        create_interface("g1/0", "2001:100:1:2::1/64", "R1"),
        create_interface("g2/0", "2001:100:1:1::1/64", "R3"),
        create_interface("g3/0", "2001:100:1:4::2/64", "R5")
    ]),
    create_router("R3", "RIP", "111", "1.1.1.3", "2001:111::3/128",[
        create_interface("g1/0", "2001:100:1:1::2/64", "R2"),
        create_interface("g2/0", "2001:100:1:8::1/64", "R4"),
        create_interface("g3/0", "2001:100:1:6::1/64", "R6"),
        create_interface("g4/0", "2001:100:1:7::1/64", "R7")
    ]),
    create_router("R4", "RIP", "111", "1.1.1.4", "2001:111::4/128",[
        create_interface("g1/0", "2001:100:1:8::2/64", "R3"),
        create_interface("g2/0", "2001:100:1:9::2/64", "R6"),
        create_interface("f0/0", "2001:100:3:1::1/64", "R8")
    ]),
    create_router("R5", "RIP", "111", "1.1.1.5", "2001:111::5/128",[
        create_interface("g1/0", "2001:100:1:3::2/64", "R1"),
        create_interface("g2/0", "2001:100:1:5::1/64", "R6"),
        create_interface("g3/0", "2001:100:1:4::1/64", "R2")
    ]),
    create_router("R6", "RIP", "111", "1.1.1.6", "2001:111::6/128",[
        create_interface("g1/0", "2001:100:1:5::2/64", "R5"),
        create_interface("g2/0", "2001:100:1:10::2/64", "R7"),
        create_interface("g3/0", "2001:100:1:6::2/64", "R3"),
        create_interface("g4/0", "2001:100:1:9::1/64", "R4")
    ]),
    create_router("R7", "RIP", "111", "1.1.1.7", "2001:111::7/128",[
        create_interface("g1/0", "2001:100:1:10::1/64", "R6"),
        create_interface("g2/0", "2001:100:1:7::2/64", "R3"),
        create_interface("f0/0", "2001:100:3:3::1/64", "R14")
    ]),
    create_router("R8", "OSPF", "112", "2.2.2.8", "2001:112::8/128", [
        create_interface("g1/0", "2001:100:2:1::1/64", "R9"),
        create_interface("g2/0", "2001:100:2:3::1/64", "R13"),
        create_interface("f0/0", "2001:100:3:1::2/64", "R4")
    ]),
    create_router("R9", "OSPF", "112", "2.2.2.9", "2001:112::9/128", [
        create_interface("g1/0", "2001:100:2:1::2/64", "R8"),
        create_interface("g2/0", "2001:100:2:2::2/64", "R14"),
        create_interface("g3/0", "2001:100:2:5::2/64", "R10"),
        create_interface("g4/0", "2001:100:2:4::2/64", "R13")
    ]),
    create_router("R10", "OSPF", "112", "2.2.1.0", "2001:112::10/128", [
        create_interface("g1/0", "2001:100:2:5::1/64", "R9"),
        create_interface("g2/0", "2001:100:2:8::2/64", "R12"),
        create_interface("g3/0", "2001:100:2:9::1/64", "R11"),
    ]),
    create_router("R11", "OSPF", "112", "2.2.1.1", "2001:112::11/128", [
        create_interface("g1/0", "2001:100:2:9::2/64", "R10"),
        create_interface("g2/0", "2001:100:2:10::2/64", "R12"),
    ]),
    create_router("R12", "OSPF", "112", "2.2.1.2", "2001:112::12/128", [
        create_interface("g1/0", "2001:100:2:7::1/64", "R13"),
        create_interface("g2/0", "2001:100:2:8::1/64", "R10"),
        create_interface("g3/0", "2001:100:2:10::1/64", "R11"),
    ]),
    create_router("R13", "OSPF", "112", "2.2.1.3", "2001:112::13/128", [
        create_interface("g1/0", "2001:100:2:6::2/64", "R14"),
        create_interface("g2/0", "2001:100:2:3::2/64", "R8"),
        create_interface("g3/0", "2001:100:2:7::2/64", "R12"),
        create_interface("g4/0", "2001:100:2:4::1/64", "R9")
    ]),
    create_router("R14", "OSPF", "112", "2.2.1.4", "2001:112::14/128", [
        create_interface("g1/0", "2001:100:2:6::1/64", "R13"),
        create_interface("g2/0", "2001:100:2:2::1/64", "R9"),
        create_interface("f0/0", "2001:100:3:2::2/64", "R7"),
    ]),
]

json_data = {"data": routers}

with open("Topology/Sujet/network_topology.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print("JSON file created: network.json")
