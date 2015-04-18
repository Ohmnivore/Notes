# Chapter 1: I skipped a bunch of boring stuff (up to page 30)
* It talked about ethical hacking - ugh
* Also talked about the pentest process, as if
it wasn't obvious enough
* Check out http://www.pentest-standard.org/ though

## Types of Penetration Tests
### Overt Penetration Testing
* Work with the organization
* In cooperation with organization's IT personnel
* May not be representative of an actual attack
* May not measure incident response accurately
* Less time and effort invested
### Covert Penetration Testing
* Performed without the knowledge of most of the
organization
* Tests the internal security team
* Takes more effort than overt pentest
* Usually preferred method

## Vulnerability Scanners
* Fingerprints OS information
* Great to identify out-of-date software

# Chapter 2: Metasploit Basics
## Terminology:
* Exploit: mean by which one takes advantage of a flaw
* Payload: code to be executed after delivery by the
framework
* Shellcode: set of instructions used as a payload
when exploitation occurs (usually in assembly language)
* Module: piece of software used by the Metasploit
Framework
* Listener: Metasploit component which listens for
an incoming connection

## Metasploit Interfaces
### MSFconsole
* The most popular interface
* Provides an interface to almost every option and
setting in the Framework
* Launched by running `mfconsole` in a command line
* `help <topic>` to get help file in mfconsole

### MSFcli
* Similar to mfconsole, but focuses on scripting
* Compatible with other command line commands, supports
redirection for example
* `msfcli -h` to display help message

### Armitage
* GUI interface
* run with `armitage` command, then select **Start MSF**

## Metasploit Utilities
### MSFpayload
* Allows to generate shellcode, executables, etc to use
outside of the Framework
* `msfpayload -h`

### MSFencode
* Fixes null characters in code
* `msfencode -h`
* x/86/shikataga_nai encoder is excellent

### Nasm Shell
* Helps analyzing assembly code
* `./nasm_shell.rb`

## Metasploit Express and Metasploit Pro
* These are commercial web interfaces
* Include a few extra tools
* Not worth it unless you do pentest for a living, and
even then...

# Chapter 3: Intelligence Gathering
* Gain accurate information about your targets without
revealing your presence or intentions

### Passive Information Gathering
* Passive and indirect: don't touch the target's systems
* Open source intelligence (OSINT)
* Yeti, whois

### whois Lookups
* `whois secmaniac.net`
* Check out DNS server hosts. They're often hosted by
a different company, but large organizations sometimes
host their own DNS servers which can be exploited

### Netcraft
* Finds IP address of a server hosting a particular
website

### NSLookup
* `nslookup set type=mx > secmaniac.net`
* Mail server info

## Active Information Gathering
* Interacting directly with a system to learn more about
it
* Must be carefully done, as it is easy to discover

### Port Scanning with Nmap
* Port scanning: connecting to ports on an IP address
one by one to detect open ports
* Identifies running services on a host
* `nmap`, -sS to stealth TCP scan, and -Pn to not use
ping
* Use -A to get more advanced Service info

### Working with Databases in Metasploit
* Metasploit supports both MySQL and PostgreSQL (default)
* `/etc/init.d/postgresql-8.3 start` to start
PostgreSQL
* In msfconsole: `db_connect
postgres:toor@127.0.0.1/msfbook`
* `dbstatus` to check connection

### Importing Nmap Results into Metasploit
* `nmap -Pn -SS -A -oX Subnet1 192.168.1.0/24` generates
Subnet1.xml file
* msfconsole `db_import Subnet1.xml` to import
* `db_hosts -c address` to check

### Advanced Nmap Scanning: TCP Idle Scan
* Stealth by spoofing IP address of another host
on the network
* Uses incremental IP IDs
* msfconsole `use auxiliary/scanner/ip/ipidseq`
* `show options`
* `set RHOSTS 192.167.1.0/24` to set RHOSTS to
192.168.1.0/24
* `run`
* -sI <IP Address> to specify the idle host

### Runninh Nmap from MSFconsole
* `fb_connect postgres:toor@127.0.0.1/msf3`
* `db_nmap` runs nmap and automatically stores results
* `db_services to check`

### Port Scanning with Metasploit
* Pivoting - using internally connected systems to route
traffic, ex: bypassing NAT
* `search portscan`
* for example, `use scanner/portscan/syn`
* `set RHOSTS 192.168.1.155`
* `run`

## Targeted Scanning
* Targeted scans look for particular OS, services,
program versions, or configs

### Server Message Block Scanning
* Often unused and poorly configured
* SMB
* `use scanner/smb/smb_version`
* `show options`
* `set RHOSTS 192.168.1.155`
* `run`
* `db_hosts -c address,os_flavor` to check

### Hunting for Poorly Configured Miscrosoft SQL Servers
* Often poorly configured
* `use scanner/mssql/mssql_ping`
* `show options`
* `set RHOSTS 192.168.1.0/24`
* `run`

### SSH Server Scanning
* Pretty secure, but older versions have vulnerabilities
* `use scanner/ssh/ssh_version`
* `set THREADS 50`
* `run`

### FTP Scanning
* FTP is often the easiest way into a target network
* `use scanner/ftp/ftp_version`
* `show options`
* `set RHOSTS 192.168.1.0/24`
* `run`
* Now let's check if it allows anonymous logins:
`use auxiliary/scanner/ftp/anonymous`

### Simple Network Management Protocol Sweeping
* Offers considerable information about devices
* `scanner/snmp/snmp_enum`
* RO (read-only) and RW (read/write) community
strings (passwords)
* SNMPv1 and v2 are unsecure, v3 is a lot more secure
* `scanner/snmp/snmp_login` tries a wordlist
to guess the community string

### Writing a Custom Scanner
* Mixins offered by Metasploit are pre-defined code
* Written in ruby
* If saved in `modules/auxiliary/scanner/http` as
simple_tcp.rb, call using `use
auxiliary/scanner/simple_tcp`

# Chapter 4: Vulnerability Scanning
* Vulnerability scanner is an automated program
designed to look for weaknesses in computers, systems,
networks, and applications
* Sends data and analyzes responses

### The Basic Vulnerability Scan
* Banner grabbing = connecting and reading service
identification
* `nc 192.168.1.203 80`

## Scanning with NeXpose
* Developed by Rapid7 (owner of Metasploit)
* Community and commercial editions available

### Configuration
* Install NeXpose
* Navigate to *https://<youripaddress>:3780*
* Accept self-signed certificate
* Login
* Tabs:
 * Assets: displays details of scans
 * Reports: vulnerability reports after they have been
 generated
 * Vulnerabilities: details on vulnerabilities discovered
 during scan
 * Administration: configuration

### The New Site Wizard
* Click **New Site** on homepage
* Add device IPs, click **Next**
* Select scan templates, click **Next**
* Add credentials if you have them
* Verify credentials using **New Login** and
**Test Login**

### The New Manual Scan Wizard
* Click **New Manual Scan**
* Double-check the IP address, then click **Start Now**
* NeXpose will now run the scan
* Wait until both Scan Progress and Discovered Assets
show *Completed*

### The New Report Wizard
* Click **New Report** in the Reports tab
* Select **NeXpose Simple XML Export** for compatibility
with Metasploit, click **Next**
* Add included devices using **Select Sites**, then
**Save**

### Importing Your Report into Metasploit Framework
* Create a new database:
 * `db_connect postgres:toor@127.0.0.1/msf3`
* Import NeXpose XML:
 * `db_import /tmp/host_195.xml`
* Test:
 * `db_hosts -c address,svcs, vulns`
 * `db_vulns`

### Running NeXpose Within MSFconsole
* Delete existing database: `db_destroy
postgres:toor@127.0.0.1/msf3`
* Create a new database: `db_connect
postgres:toor@127.0.0.1/msf3`
* Load NeXpose plugin: `load nexpose`
* Connect to local NeXpose install:
`nexpose_connect`
* Initiate scan: `nexpose_scan 192.168.1.195`
* Check with `db_hosts -c address` and `db_vulns`

## Scanning with Nessus
* Developed by Tenable Security

### Nessus Configuration
* After installation, navigate to
*https://<youripaddress>:8834*
* Accept certificate warning
* Log into Nessus

### Creating a Nessus Scan Policy
* In Policies tab, click **Add** button
* This is seriously intuitive and obvious, so I'll skip
the rest of these instructions

### Running a Nessus Scan
* Go to **Scans** tab, click **Add**
* Edit options, then click **Launch Scan**

### Nessus Reports
* After a scan is complete it becomes a new entry
in the Reports tab
* Find a report and click **Browse**

### Importing Results into the Metasploit Framework
* Click **Download Report** in Reports tab
* Select default (.nessus) file format
* `db_connect postgres:toor@127.0.0.1/msf3`
* `db_import /tmp/nessus_report_Host_195.nessus`
* `db_hosts -c address,svcs,vulns`
* `db_vulns`

### Scanning with Nessus from Within Metasploit
* Nessus Bridge plugin by Zate
* `db_destroy postgres:toor@127.0.0.1/msf3`
* `db_connect postgres:toor@127.0.0.1/msf3`
* `load nessus`
* `nessus_help`
* `nessus_connect dookie:s3cr3t@192.168.1.101:8834` to
authenticate
* `nessus_policy_list`
* `nessus_scan_new`
* `nessus_scan_new 2 bridge_scan 192.168.1.195`
* `nessus_scan_status`
* `nessus_report_list`
* `nessus_report_get` to import report into database

## Specialty Vulnerability Scanners
### Validating SMB Logins
* SMB Login Check Scanner
* Loud and noticeable, shows in Windows logs
* `use smb_login`
* `show_options`

### Scanning for Open VNC Authentication
* Virtual network computing (VNC) = graphical access
to remote system
* Old versions leave default password blank
* VNC Authentication None scanner
* `use auxiliary/scanner/vnc/vnc_none_auth`
* Use vncviewer to connect

### Scanning for Open X11 Servers
* open_x11 scanner
* X11 not widely used nowadays
* xspy tool to exploit X11 vulnerabilities

### Using Scan Results for Autopwning
* Autopwn tool automatically targets and exploits a
system using an open port or results of a vuln scan
* Create new Metasploit database
* Import a scan report to the database
* `db_autopwn -etrxp`
 * e: all targets
 * t: show all matching modules
 * r: reverse shell payload
 * x: select exploit modules based on vulnerability
 * p: select exploit modules based on open ports
* Successful exploit returns a shell to the attacking
machine
* `db_autopwn -h` for help

# Chapter 5: The Joy of Exploitation
* We'll be using msfconsole, msfencode, and msfpayload

## Basic Exploitation
* Running `show` from msfconsole will display every
available module

### msf> show exploits
* Exploits operate against vulnerabilities discovered
during a penetration test

### msf> show auxiliary
* Auxiliary modules used for scanning, DoS, fuzzers,
etc.

### msf> show options
* Shows module options when one is selected
* Otherwise shows global options
* Use `back` command to exit a module
* Use `search` to find a specific attack, auxiliary
module, or payload

### msf> show payloads
* Payload = platform-specific portion of code
delivered to a target
* If module is selected, this command shows only
compatible payloads
* If running an exploit, it shows only payloads
applicable to the attack
* `set payload <name>`
* `show options`

### msf> show targets
* When module selected, shows vulnerable potential
targets compatible with it
* Automatic targeting isn't always the best idea because
it might crash the system or simply not work if it's
wrong

### info
* Gets detailed information about a module

### set and unset
* `set` to set an option
* `unset` to turn off a setting

### setg and unsetg
* Same as set and unset, but operate on global settings

### save
* Saves global settings

## Exploiting Your First Machine
