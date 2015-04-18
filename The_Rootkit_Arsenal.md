# Preface
* Part 1: Core framework
* Part 2: Postmortem forensics
* Part 3: Live response
* Part 4: Summation

### Prerequisites
* C
* Intel assembly

#Part 1: Foundation
# Chapter 1: Empty Cup Mind
* Rootkit = kit for maintaining root privileges
* Attack cycle
 * Information gathering
 * Gain access to a command interface
 * Escalate rights
 * Deploy rootkit
 * Command and Control
* Pivoting: using other machines in a compromised network

### Droppers
* Exploit -> payload -> dropper -> installation
* Multi-stage dropper: downloads the rootkit instead
of being bundled with it
* Rootkit = tool that hides itself and other process/data/
activity on a system
 * Used for concealment
 * Command and control (C2)
 * Surveillance
* Good rootkits are designed to stay secret, so the admin
will never notice them

## Infectious Agents
* Viruses
 * Need to be actively executed by the user
 * Infects other files
 * Ex: disquette boot sector, email attachments, browser-
 based ActiveX, warez
* Worms
 * In contrast to viruses, they spread automatically
 * Ex: Morris Worm
* Adware
 * Displays ads when executed or installed
 * Ex: Eudora back in the day
* Spyware
 * Collects information about the user without consent
 * Ex: Hotbar

### Rise of the Botnets
* Collection of compromised machines
* Controlled remotely by someone
* Command and control servers (C2) used to control: IRC
or web servers with high bandwidth
* Bot software usually delivered as a payload within
malware
* Botnets can send spam, phishing scams, DDoS attacks,
etc.
* 150 million of the 600 million computers connected to
the Internet belong to a botnet
* In 2005 the Netherlands police uncovered a botnet
consisting of 1.5 million machines

### Enter: Conficker
* Botnet with 10 million infected hosts
* Microsoft offered $250,000 reward for information about
its authors

### Malware Versus Rootkits
* Rootkits are solely concerned with sustaining covert
access to a machine, not self-propagation for example
* Rootkits can be fused with malware as a *force
multiplier*

### Who Is Building and Using Rootkits
* Data is the new currency
* Marketing
* Digital Rights Management (DRM enforcing, *cough,
cough, SONY, cough cough*)
* Rootkits as features, ex: Symantec's SystemWorks
* Law enforcement, ex: Magic Lantern
* Industrial Espionage
* Political Espionage
* Cybercrime

### Who Builds State-of-the-Art Rootkits?
* Intelligence agencies

# Chapter 2: Overview of Anti-Forensics
* Goal of AF is to minimize the quantity and quality of
useful trace evidence
* Rootkits and AF go hand in hand
* Sometimes the point isn't to erase all traces, but to
make it difficult and expensive to find them

## Incident Response
* IR = emergency response for suspicious computer events

### Intrusion Detection System
* IDS = unared, off-duty cop doing a security guard
night shift
* Sounds the alarm when something's suspicious
* Two types
 * HIDS: host-based, scans for malware locally
 * NIDS: sits on the network, scans packets
* Intrusion prevention system is like an IDS, but it
takes action once it detects a threat

## Computer Forensics
Goals:
* Identify attacker
* Identify what the attacker did
* When the attack happened
* How the attack was carried out
* Why the attack was carried out

## Why AF?
Lots of sys admins will just nuke a compromised machine:
* Shut down
* Flash firmware
* Wipe drive
* Rebuild from a prepared disk image

**BUT** forensic analysis can also be used
*preemptively*

### Classifying Forensic Techniques: First Method
* Data can reside locally, on a remote machine, or on the
network
* Volumes -> file systems (ex: NTFS, FAT) -> files ->
type of file (executable, text-based, config, etc.)

### Classifying Forensic Techniques: Second Method
* The order of volatility
 * "When collecting evidence you should proceed from
 the volatile to the less volatile"
* Locard's exchange principle: "every contact leaves a
trace", the very act of collecting data can disturb the
crime scene

### Live Response
* Often involves dumping the contents of the memory
* Volatile data = information that will be lost if the
machine lost power
* Port scans can be performed
* Process memory images

### When Powering Down Isn't an Option
* To create a crash dump or not? That is the question.
* Keep the machine on to monitor the intruder?

### The Debate over Pulling the Plug
* Normal shutdown vs yanking the power cable or battery
* Shutting down = less risk of corrupting the file system
 * But it allows shutdown scripts and the like to run
 so an attacker can cover his tracks
* Some attackers can shut down the machine themselves
to destroy evidence, so yanking the power can avoid that

### To Crash Dump or Not to Crash Dump
* Crash dumps offer insight into the system's internal
structures
* Kernel debuggers
* Crash dumps are disruptive if saved to the same drive
that is being investigated

### Postmortem Analysis
* BIOS and PCI-RIM snapshots can be taken for analysis

## AF Strategies
f = file, fs = filesystem
* Data destruction: f scrubbing, fs attacks
* Data conceilment: in-band, out-of-band, app layer
conceilment
* Data transformation: compression, encryption,
code morphing, direct edits
* Data fabrication: introduce known files, string
decoration, false audit trails
* Data source elimination: data contraception, custom
module loaders

* Buy time with data source elimination and data
destruction
* Leave difficult to capture and understand evidence
with data conceilment and data transformation
* Plant misinformation and decoy investigation paths
with data fabrication

### Data Destruction
* Ex: wiping memory buffers used by a program,
repeated overwriting
* Data transformation can be used for data destruction
* Dissolving batch file
* In Windows, a binary can't delete itself, but can
make an executable to do that on its behalf

### Data Concealment
* Storing data in a manner that it's not likely to be
found
* Security through obscurity
* Only works on the short term
* Ex: storing files in the System Volume Information
folder
* Active conceilment = modifying host operating system
after launch

### Data transformation
* Ex: steganography, ciphers, encryption
* Armoring: rootkit is stored as an encrypted executable
that decrypts itself at runtime
* English shellcode: conceil machine instructions as
ASCII text

### Data Fabrication
* Generate false positives and bogus leads
* Buys time

### Data Source Elimination
* Don't rely on the targeted system
 * ex: not registered for execution by the kernel

## General Advice for AF Techniques
### Use Custom Tools
* Metasploit and UPX are awesome, but they've already
been analyzed to death

### Low and Slow versus Scorched Earth
* The goal of AF is to buy time
* Noisy way:
 * Ex: flood the system with malware or a few gigs of
 drivers (divert suspicion from a rootkit)
 * However, it alerts the investigator that something
 is wrong
* Instead, rootkits should only use those AF tools
that are conducive to sustaining a minimal profile
* Don't raise any red flags

### Shun Instance-Specific Attacks
* A skilled forensic investigator doesn't limit himself
to his tools

### Use a Layered Defense
* We assume that forensic tools are being deployed
preemptively
* Make automation as hard as possible

## John Doe Has the Upper Hand
* Black Hats have the upper hand for now

### Attackers Can Focus on Attacking
* Attackers have only one concern: breaking in
* Defenders have the hurdle of the business aspect

### Defenders Face Institutional Challenges
* Investigators often mired by bureaucracy

### Security Is a Boring Process

### Ever-Increasing Complexity
* New versions of operating systems aren't becoming more
secure
* Old dependencies remain security flaws
* TL;DR Microsoft is shit at patching vulnerabilities

## Conclusions
* AF
 * Leave behind as little useful evidence as possible
 * Make the evidence that remains difficult to capture
 and understand
 * Plant misinformation
* Rootkits are a subset of AF that rely on low-and-slow
strategies
 * Provide remote access
 * Provide monitoring
 * Provide concealment
* Rootkit architecture:
 * What part of the system it interfaces with
 * Where the rootkit will reside

# Chapter 3: Hardware Briefing
* For writing rootkits, one must choose the Windows
execution mode(s) to use

## Physical Memory
* IA-32 processor family -> accesses bytes (8 bits)
using a unique *physical address* (an integer)
* Physical address range = *physical address space*
* Physical addresses start at 0 and increment by 1
* Low memory: addresses near 0
* High memory: addresses near the final byte
* Control bus and data bus to r/w physical memory
* Read operation steps:
 * Processor places address to be read on the address
 lines
 * Processor send the read signal to the control bus
 * RAM chips return the byte on the data bus
* Write operation steps:
 * Processor places the address to be written on the
 address lines
 * Processor send the write signal on the control bus
 * Processor sends the byte to be written on the data bus
* IA-32 r/w 4 bytes at a time

## IA-32 Memory Models
### Flat memory model
* Abstraction
* Memory = contiguous sequence of bytes
 * Addressed starting from 0
 * Ending at arbitrary value *N*, 2^32 - 1 in IA-32
* Address of a byte = *linear address*
* Range of possible bytes = *linear address space*
* Similar to physical memory, only difference is that
it's at a higher level of abstraction

### Segmented Memory Model
* Regions of memory, aka segments
* Byte of an address = *logical address*
* Logical address consists of:
 * *Segment selector*
 * *Effective address/Offset address*: position of byte
 in the segment

### Modes of Operation
* Modes
 * Real mode
 * Protected mode
 * System management mode
* Real mode
 * 16-bit execution environment
 * Old Intel 8086/88 backwards compatibility
 * Used on power up
* Protected mode:
 * Execution environment for system software like Win 7
* System management mode (SMM):
 * Executes special code embedded in the firmware
  * Emergency shutdown
  * Power management
  * System security
  * Etc.
* We're interested in real mode and protected mode,
which use a segmented memory model
* Real mode -> segmentation without protection
* Protected mode -> memory protection facilities
* SMM -> advanced topic, will be discussed later

## Real Mode
* Segmeneted memory model
* 20-bit address space
* Originally used by 8086/88 processors
* Logical address
 * 16-bit segment selector -> base address of a 64-KB
 memory segment
 * 16-bit effective address -> offset added to the
 segment selector
* Segment address has an implicit 0 added to the end
 * 0x2000 becomes 0x20000
* Processor accesses at most 1MB of physical memory
* No memory protection
* User application can modify the underlying operating
system

### Case Study: MS-DOS
* First 640 KB of memory = *conventional memory*
(system-level code)
* Remaining (up until 1MB) memory = *upper memory area*
(UMA) (reserved space for use by hardware)
* *Upper memory blocks* (UMBs) = unused slots in the UMA
* Memory above 1MB is called *extended memory*
* `mem.exe`/`mem.exe /d` for address space overview

### Why Study Real Mode?
* BIOS and boot code operate in real mode
* Real mode lays the basics for protected mode

### The Real-Mode Execution Environment
* 16-bit registers:
 * 6 segment registers
  * Store segment selectors
  * CS, DS, SS, ES
 * 4 general registers
  * Store numeric operands or address values
  * AX, BX, CX, DX
 * 3 pointer registers
  * Store effective addresses
  * IP, SP, BP
 * 2 indexing registers
  * Store indexing addressing, string and mathematical
  operations
  * SI, DI
 * 1 FLAGS register
  * Store CPU status or result of an operation
  * Only 9 bits are used
  * TF; bit 8 (trap flag), IF; bit 9 (interrupt enable)
  * If TF is 1, single-step interrupt after each
  instruction
  * If IF is set, interrupts are acknowledged and
  acted upon
* See Table 3.2 (list of registers and their purposes)
* Use `debug.exe` to view the state of the registers

### Real-Mode Interrupts
* *Interrupt* = event that triggers an *interrupt
service* routine (ISR), also known as *interrupt handler*
* First KB of memory (0x00000 to 0x003FF) is occupied
by the *interrupt vector table* (IVT) -> *interrupt
descriptor table* (IDT) in protected mode
* The IVT and IDT map interrupts to ISRs
 * Store a series of *interrupt descriptors* or
 *interrupt vectors* in real mode that designate
 the ISR's location in memory
 * IVT stores logical address of each ISR sequentially
 * At 0x00000 is the effective address of the first
 ISR followed by its segment selector (low byte comes
 first for both)
 * Each interrupt takes 4 bytes to store
 * Max 256 vectors (0 to 255)
* Three types of interrupts:
 * Hardware (maskable and nonmaskable)
 * Software interrupts
 * Exceptions (faults, traps, aborts)
* Hardware interrupts
 * Generated by external devices and unanticipated
 * Maskable = can be disabled by clearing the IF using
 the `CLI` instruction
  * Ex: 8 (system timer), 9 (keyboard)
 * Nonmaskable = can't be disabled and CPU always acts on
 it
  * Ex: 2
* Software interrupts (internal interrupts)
 * `INT [int]` instruction
* Exception interrupts
 * Generated when processor detects an error while
 executing an instruction
 * Fault: allows instruction restart, reports at the
 preceding instruction boundary
 * Trap: no instruction restart, reports at the
 following instruction boundary
 * Abort: the program cannot be restarted

### Segmentation and Program Control
* Real mode uses segmentation to manage memory
* For jump instructions
 * `JMP, CALL, RET, RETF, INT, IRET`
 * near (intrasegment) are within the same segment
 * far (intersegment) are within other segments
 * `INT, IRET` always far jumps
 * `JMP, CALL` near or far depending on context
  * can also be direct or indirect (specify destination)
  of jump or not

### Case Study: Dumping the IVT
Check source code

### Case Study: Logging Keystrokes with a TSR
