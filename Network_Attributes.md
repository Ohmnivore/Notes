# Notes
This is a WIP

# MAC address
* Every 802.x card has one.
* 48-bit integer
* Networking equipment remembers this address after an authentication
* It figures in unpurgeable logs, ISP logs, manufacturer logs, etc.
* Spoofing your MAC address requests a new IP from your ISP, acting like
an IP address reset
* MAC is confined to the LAN

### Changing your MAC address
**Linux:**

```
ifconfig eth0 down
macchanger -r eth0
ifconfig eth0 up
```

**Windows:**
Find yer own tools

# 802.11 "Nickname"
**Linux:**

```
iwconfig ath0 nickname "Anon"
```
**Windows:**
Change machine hostname: modify registry or find other means

# DHCP Properties
* Used when obtaining an IP address
* Includes hostname, MAC address, sometimes OS info and DHCP version
* Compromises anonimity in LAN
* Provides most recent IP address to DHCP server
* You must therefore wipe out previous IP leases

### Hiding revealing information
**Linux:**
Varies between distros, but DHCP info is often read from
`/etc/dhclient-interface.conf`

Change `/etc/init.d/net.eth0` file or its equivalent to

```
VID=`fortune -o|head -c 30|tr "\"'\n" ' ' 2>/dev/null`
/sbin/dhcpcd -i ${VID} ${dhcpcd_IFACE} ${IFACE}
```

Previous IPs found in `/var/lib/dhcp/` -> do this between restarts:

```
/sbin/ifdown ethN ;
[change mac addr] ;
[change hostname] ;
rm /var/lib/dhcp/* ;
/sbin/ifup ethN ;
```

**Windows:**
Change your hostname to something that won't identify you
(through registry or other means)

```
ipconfig /release
ipconfig /renew
```

# IP Address
### Proxy hopping
* Not very effective unless done exactly right with exactly the right
proxies
* Find proxies that don't report your IP address in the form of
a cookie/session variable to hosts
* The above issue can tested through various checkers
* It's possible to chain multiple proxies together

### SSH Hopping
*
