import csv,argparse,sys

def readdata(filename):
    r=[]
    with open(filename,"rt") as file:
        reader = csv.DictReader(file)
        for e in reader:
            r.append(e)
    return r


# Firewall User Group
# FortiManager OS v6.4: Policy & Objects -> Object Configurations -> User & Authentication -> User Groups
# Fortigate OS v6.4: User & Authentication -> User Groups
def UserGroupGen(listofentries):
    print(f"config user group")
    for e in listofentries:
        print(f"edit \"{e['Group Name']}\"")
        print(f"  set member 8445PE2VDC001 8445PE2VDC002")
        print(f"  config match")
        print(f"    edit 1")
        print(f"      set server-name 8445PE2VDC001")
        print(f"      set group-name \"{e['DistinguishedName']}\"")
        print(f"    next")
        print(f"    edit 2")
        print(f"      set server-name 8445PE2VDC002")
        print(f"      set group-name \"{e['DistinguishedName']}\"")
        print(f"    next")
        print(f"  end")
        print(f"next")
    print(f"end")


# Firewall Address Group
# FortiManager OS v6.4: Policy & Objects -> Object Configurations -> Firewall Objects -> Addresses
# Fortigate OS v6.4: Policy & Objects -> Addresses
def AddAddressToGroup(listofentries,groupname):
    print(f"config firewall addrgrp")
    print(f"  edit \"{groupname}\"")
    print(f"    set member",end='')
    for e in listofentries:
        if e['IP']:
            print(f" \"{e['Name']}\"",end='')
    print(f"")    
    print(f"  next")
    print(f"end")


# Firewall Address
# FortiManager OS v6.4: Policy & Objects -> Object Configurations -> Firewall Objects -> Addresses
# Fortigate OS v6.4: Policy & Objects -> Addresses
def FirewallAddressGen(listofentries):
    print(f"config firewall address")
    for e in listofentries:
        if e['IP']:
            print(f"  edit \"{e['Name']}\"")
            print(f"    set subnet {e['IP']} {e['SubnetMask']}")
            print(f"  next")
    print(f"end")


# Firewall Policy
# FortiManager OS v6.4: Policy & Objects -> Policy Packages -> Firewall Policy
# Fortigate OS v6.4: Policy & Objects -> Firewall Policy
def FirewallPolicyGen(listofentries):
    print(f"config firewall policy")
    for e in listofentries:
        print(f"edit {e['Rule Number']}")
        print(f"  set name {e['Name']}")
        print(f"  set srcintf {e['Source Interface']}")
        print(f"  set dstintf {e['Destination Interface']}")
        print(f"  set srcaddr {e['Source Address']}")
        print(f"  set dstaddr {e['Destination Address']}")
        print(f"  set action {e['Action']}")
        print(f"  set schedule {e['Schedule']}")
        print(f"  set service {e['Service']}")
        print(f"  set logtraffic {e['Log Traffic']}")
        print(f"  set groups {e['Group']}")
        print(f"next")
    print(f"end")


#
def main():
    parser=argparse.ArgumentParser(description='Fortigate Configuration Generator')
    parser.add_argument('-d','--data',type=str,metavar='',required=True,help='Data file, csv format')
    parser.add_argument('-t','--type',type=str,metavar='',help='Type of configuration: group, policy')
    group=parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet',action='store_true', help='print quiet')
    group.add_argument('-v', '--verbose',action='store_true', help='print verbose')
    args=parser.parse_args()

    if args.data and args.type == "group":
        data = readdata(args.data)
        UserGroupGen(data)
    elif args.data and args.type== "policy":
        data = readdata(args.data)
        FirewallPolicyGen(data)
    elif args.data and args.type=="address":
        data = readdata(args.data)
        FirewallAddressGen(data)
    elif args.data and args.type=="addresstogroup":
        groupname="SchoolFortigates"
        if groupname=="":
            print(f"Missing Group Name")
            sys.exit(1)
        data = readdata(args.data)
        AddAddressToGroup(data,groupname)
    else:
        print(f"Wrong syntax")


if __name__ == "__main__":
    main()


