# Fortigate Configuration Generator
## Usage
- python3 configgen.py -h

## Generate Firewall User Grouop
- python3 configgen.py -d $csvfile -t group
- CSV file header: Group Name,DistinguishedName

### Sample config
```python
config user group
edit "Group Name"
  set member Server1 Server2
  config match
    edit 1
      set server-name Server1
      set group-name "CN=Group Name,OU=Groups,OU=Staff,DC=domain,DC=com"
    next
    edit 2
      set server-name Server2
      set group-name "CN=Group Name,OU=Groups,OU=Staff,DC=domain,DC=com"
    next
  end
next
end
```

## Generate Firewall Policy
- python3 configgen.py -d $csvfile -t policy
- CSV file header: Rule Number,Name,Source Interface,Destination Interface,Source Address,Destination Address,Action,Schedule,Service,Log Traffic,Group,Comments

### Sample config
```python
config firewall policy
edit 907
  set name Policy Name
  set srcintf Source_Interface
  set dstintf Destination_Interface
  set srcaddr Source_address
  set dstaddr Destination_address
  set action accept
  set schedule always
  set service DNS HTTP HTTPS PING RDP SSH TELNET TRACEROUTE
  set logtraffic all
  set groups Group_name
next
```