import csv,argparse

def readdata(filename):
    r=[]
    with open(filename,"rt") as file:
        reader = csv.DictReader(file)
        for e in reader:
            r.append(e)
    return r

def usergroupgen(listofentries):
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
    
def firewallpolicygen(listofentries):
    print(f"config firewall policy")
    for e in listofentries:
        print(f"edit {e['Rule Number']}")
        print(f"  set name {e['Name']}") #VPN to 8497 St Thomas More"
        print(f"  set srcintf {e['Source Interface']}") #ssl.INTERNET"
        print(f"  set dstintf {e['Destination Interface']}") #vdroot-INT0"
        print(f"  set srcaddr {e['Source Address']}") #CEWAPE2VPN-10.65.0.0/16"
        print(f"  set dstaddr {e['Destination Address']}") #School-8497-LAN"
        print(f"  set action {e['Action']}") #accept
        print(f"  set schedule {e['Schedule']}") #always"
        print(f"  set service {e['Service']}") #"DNS" "HTTP" "HTTPS" "PING" "RDP" "SSH" "TELNET" "TRACEROUTE"
        print(f"  set logtraffic {e['Log Traffic']}") #all
        print(f"  set groups {e['Group']}") #PE2VPNGroup-User-8497"
        print(f"next")
    print(f"end")

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
        usergroupgen(data)
    elif args.data and args.type== "policy":
        data = readdata(args.data)
        firewallpolicygen(data)
    else:
        print(f"Wrong syntax")

if __name__ == "__main__":
    main()


