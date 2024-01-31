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
    # AS 59520
    create_router("R1", "OSPF", "59520", "5.9.5.1", "2001:5952::1/128", [
        create_interface("g2/0", "2001:5952:2::2/64", "R2")
    ]),
    create_router("R2", "OSPF", "59520", "5.9.5.2", "2001:5952::2/128", [
        create_interface("g1/0", "2001:5952:2::1/64", "R1"),
        create_interface("g2/0", "2001:5952:3::2/64", "R3"),
        create_interface("f0/0", "2001:10::1/64", "R9", local_pref="120")
    ]),
    create_router("R3", "OSPF", "59520", "5.9.5.3", "2001:5952::3/128", [
        create_interface("g1/0", "2001:5952:3::1/64", "R2"),
        create_interface("f0/0", "2001:80::1/64", "R4", local_pref="250")
    ]),
     # AS 76520
    create_router("R4", "OSPF", "76520", "7.6.5.4", "2001:7652::4/128",[
        create_interface("g1/0", "2001:7652:1::1/64", "R5"),
        create_interface("g2/0", "2001:7652:2::2/64", "R7"),
        create_interface("f0/0", "2001:80::2/64", "R3")
    ]),
    create_router("R5", "OSPF", "76520", "7.6.5.5", "2001:7652::5/128",[
        create_interface("g1/0", "2001:7652:1::2/64", "R4"),
        create_interface("g2/0", "2001:7652:5::1/64", "R6"),
    ]),
    create_router("R6", "OSPF", "76520", "7.6.5.6", "2001:7652::6/128",[
        create_interface("g1/0", "2001:7652:4::2/64", "R7"),
        create_interface("g2/0", "2001:7652:5::2/64", "R5"),
        create_interface("g3/0", "2001:3333::1/64", "NETWORK")
    ]),
    create_router("R7", "OSPF", "76520", "7.6.5.7", "2001:7652::7/128",[
        create_interface("g1/0", "2001:7652:2::1/64", "R4"),
        create_interface("g2/0", "2001:7652:4::1/64", "R6"),
        create_interface("f0/0", "2001:58::1/64", "R8")
    ]),
     # AS 69100
    create_router("R8", "RIP", "69100", "6.9.1.8", "2001:6910::8/128", [
        create_interface("g1/0", "2001:6910:2::2/64", "R15"),
        create_interface("f0/0", "2001:58::2/64", "R7")
    ]),
    create_router("R9", "RIP", "69100", "6.9.1.9", "2001:6910::9/128:", [
        create_interface("g1/0", "2001:6910:1::2/64", "R15"),
        create_interface("f0/0", "2001:10::2/64", "R2")
    ]),
    create_router("R10", "RIP", "69100", "6.9.1.10", "2001:6910::10/128", [
        create_interface("g1/0", "2001:6910:3::2/64", "R15"),
        create_interface("f0/0", "2001:26::1/64", "R11")
    ]),
    create_router("R15", "RIP", "69100", "6.9.1.15", "2001:6910::15/128", [
        create_interface("g1/0", "2001:6910:1::1/64", "R9"),
        create_interface("g2/0", "2001:6910:2::1/64", "R8"),
        create_interface("g3/0", "2001:6910:3::1/64", "R10"),
    ]),
     # AS 13880
    create_router("R11", "OSPF", "13880", "1.3.8.11", "2001:1388::11/128", [
        create_interface("g1/0", "2001:1388:2::2/64", "R12"),
        create_interface("f0/0", "2001:26::2/64", "R10"),
    ]),
    create_router("R12", "OSPF", "13880", "1.3.8.12", "2001:1388::12/128", [
        create_interface("g1/0", "2001:1388:1::1/64", "R14"),
        create_interface("g2/0", "2001:1388:2::1/64", "R11"),
        create_interface("g3/0", "2001:1388:3::1/64", "R13"),
    ]),
    create_router("R13", "OSPF", "13880", "1.3.8.13", "2001:1388::13/128", [
        create_interface("g1/0", "2001:1388:3::2/64", "R12"),
        create_interface("g2/0", "2001:2222::1/64", "NETWORK")
    ]),
    create_router("R14", "OSPF", "13880", "1.3.8.14", "2001:1388::14/128", [
        create_interface("g1/0", "2001:1388:1::2/64", "R12"),
        create_interface("g2/0", "2001:1111::1/64", "NETWORK")
    ]),
]

json_data = {"data": routers}

with open("Topology/Various/network_topology.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print("JSON file created: network.json")
