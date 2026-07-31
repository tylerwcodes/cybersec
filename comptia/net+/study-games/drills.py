"""Special drills: subnetting generator, port blitz, acronym blitz.

The port table and acronym list come straight from the official
N10-009 exam objectives document.
"""
import difflib
import ipaddress
import random

from engine import (C, QuitRound, banner, get_input, grade_line, normalize,
                    wrap)

# ------------------------------------------------------------------- ports ---
# (name, abbreviation, display port, acceptable answers, transport/notes)
PORTS = [
    ("File Transfer Protocol", "FTP", "20/21",
     ["20 21", "21", "20"], "TCP - 20 data, 21 control"),
    ("Secure File Transfer Protocol", "SFTP", "22",
     ["22"], "TCP - file transfer over SSH"),
    ("Secure Shell", "SSH", "22",
     ["22"], "TCP - encrypted remote CLI"),
    ("Telnet", "Telnet", "23",
     ["23"], "TCP - legacy plaintext remote CLI"),
    ("Simple Mail Transfer Protocol", "SMTP", "25",
     ["25"], "TCP - mail transfer between servers"),
    ("Domain Name System", "DNS", "53",
     ["53"], "UDP queries / TCP zone transfers"),
    ("Dynamic Host Configuration Protocol", "DHCP", "67/68",
     ["67 68", "67", "68"], "UDP - 67 server, 68 client"),
    ("Trivial File Transfer Protocol", "TFTP", "69",
     ["69"], "UDP - simple transfers, firmware/configs"),
    ("Hypertext Transfer Protocol", "HTTP", "80",
     ["80"], "TCP - unencrypted web"),
    ("Network Time Protocol", "NTP", "123",
     ["123"], "UDP - time synchronization"),
    ("Simple Network Management Protocol", "SNMP", "161/162",
     ["161 162", "161", "162"], "UDP - 161 queries, 162 traps"),
    ("Lightweight Directory Access Protocol", "LDAP", "389",
     ["389"], "TCP/UDP - directory services"),
    ("Hypertext Transfer Protocol Secure", "HTTPS", "443",
     ["443"], "TCP - web over TLS"),
    ("Server Message Block", "SMB", "445",
     ["445"], "TCP - Windows file/printer sharing"),
    ("Syslog", "Syslog", "514",
     ["514"], "UDP - log messages to a collector"),
    ("Simple Mail Transfer Protocol Secure", "SMTPS", "587",
     ["587"], "TCP - mail submission with STARTTLS"),
    ("Lightweight Directory Access Protocol over SSL", "LDAPS", "636",
     ["636"], "TCP - encrypted directory services"),
    ("Structured Query Language (SQL) Server", "SQL Server", "1433",
     ["1433"], "TCP - Microsoft SQL Server database"),
    ("Remote Desktop Protocol", "RDP", "3389",
     ["3389"], "TCP - graphical remote desktop"),
    ("Session Initiation Protocol", "SIP", "5060/5061",
     ["5060 5061", "5060", "5061"], "TCP/UDP - 5060 unencrypted, 5061 TLS (VoIP)"),
]


def port_blitz(rounds=15):
    banner("PORT BLITZ", C.MAGENTA)
    print(wrap("Memorize the official N10-009 port table. Forward and reverse "
               "questions, streak bonuses shown. Type q to stop."))
    score, streak, best_streak = 0, 0, 0
    asked = 0
    try:
        for n in range(1, rounds + 1):
            entry = random.choice(PORTS)
            name, abbr, port, accepted, notes = entry
            forward = random.random() < 0.5
            print()
            if forward:
                print(wrap(f"{n}. What port(s) does {C.BOLD}{name} ({abbr}){C.RESET} use?"))
                ans = normalize(get_input("  Port(s): "))
                ok = ans in [normalize(a) for a in accepted]
            else:
                print(wrap(f"{n}. Which protocol uses port {C.BOLD}{port}{C.RESET}?"))
                ans = normalize(get_input("  Protocol: "))
                # any protocol sharing that display port counts (SSH/SFTP on 22)
                valid = [p for p in PORTS if p[2] == port]
                names = [normalize(p[0]) for p in valid] + [normalize(p[1]) for p in valid]
                ok = ans in names
            asked += 1
            if ok:
                score += 1
                streak += 1
                best_streak = max(best_streak, streak)
                flame = " 🔥" * min(3, streak // 3)
                print(C.GREEN + C.BOLD + f"  ✔ Correct! (streak {streak}){flame}" + C.RESET)
            else:
                streak = 0
                print(C.RED + C.BOLD + f"  ✘ {abbr} = port {port}" + C.RESET)
            print(C.DIM + f"    {abbr}: {notes}" + C.RESET)
    except QuitRound:
        pass
    if asked:
        print()
        print(grade_line(score, asked))
        print(C.DIM + f"  Best streak: {best_streak}" + C.RESET)


# ---------------------------------------------------------------- acronyms ---
# Official N10-009 acronym list (objectives document, pages 16-17).
ACRONYMS = {
    "ACL": "Access Control List",
    "AH": "Authentication Header",
    "AP": "Access Point",
    "API": "Application Programming Interface",
    "APIPA": "Automatic Private Internet Protocol Addressing",
    "ARP": "Address Resolution Protocol",
    "AUP": "Acceptable Use Policy",
    "BGP": "Border Gateway Protocol",
    "BNC": "Bayonet Neill-Concelman",
    "BSSID": "Basic Service Set Identifier",
    "BYOD": "Bring Your Own Device",
    "CAM": "Content-addressable Memory",
    "CDN": "Content Delivery Network",
    "CDP": "Cisco Discovery Protocol",
    "CIA": "Confidentiality, Integrity, and Availability",
    "CIDR": "Classless Inter-domain Routing",
    "CLI": "Command-line Interface",
    "CNAME": "Canonical Name",
    "CPU": "Central Processing Unit",
    "CRC": "Cyclic Redundancy Check",
    "DAC": "Direct Attach Copper",
    "DAS": "Direct-attached Storage",
    "DCI": "Data Center Interconnect",
    "DDoS": "Distributed Denial-of-service",
    "DHCP": "Dynamic Host Configuration Protocol",
    "DLP": "Data Loss Prevention",
    "DNS": "Domain Name System",
    "DNSSEC": "Domain Name System Security Extensions",
    "DoH": "DNS over Hypertext Transfer Protocol Secure",
    "DoS": "Denial-of-service",
    "DoT": "DNS over Transport Layer Security",
    "DR": "Disaster Recovery",
    "EAPoL": "Extensible Authentication Protocol over LAN",
    "EIGRP": "Enhanced Interior Gateway Routing Protocol",
    "EOL": "End-of-life",
    "EOS": "End-of-support",
    "ESP": "Encapsulating Security Payload",
    "ESSID": "Extended Service Set Identifier",
    "EULA": "End User License Agreement",
    "FC": "Fibre Channel",
    "FHRP": "First Hop Redundancy Protocol",
    "FTP": "File Transfer Protocol",
    "GDPR": "General Data Protection Regulation",
    "GRE": "Generic Routing Encapsulation",
    "GUI": "Graphical User Interface",
    "HTTP": "Hypertext Transfer Protocol",
    "HTTPS": "Hypertext Transfer Protocol Secure",
    "IaaS": "Infrastructure as a Service",
    "IaC": "Infrastructure as Code",
    "IAM": "Identity and Access Management",
    "ICMP": "Internet Control Message Protocol",
    "ICS": "Industrial Control System",
    "IDF": "Intermediate Distribution Frame",
    "IDS": "Intrusion Detection System",
    "IoT": "Internet of Things",
    "IIoT": "Industrial Internet of Things",
    "IKE": "Internet Key Exchange",
    "IP": "Internet Protocol",
    "IPAM": "Internet Protocol Address Management",
    "IPS": "Intrusion Prevention System",
    "IPSec": "Internet Protocol Security",
    "IS-IS": "Intermediate System to Intermediate System",
    "LACP": "Link Aggregation Control Protocol",
    "LAN": "Local Area Network",
    "LC": "Local Connector",
    "LDAP": "Lightweight Directory Access Protocol",
    "LDAPS": "Lightweight Directory Access Protocol over SSL",
    "LLDP": "Link Layer Discovery Protocol",
    "MAC": "Media Access Control",
    "MDF": "Main Distribution Frame",
    "MDIX": "Medium Dependent Interface Crossover",
    "MFA": "Multifactor Authentication",
    "MIB": "Management Information Base",
    "MPO": "Multifiber Push On",
    "MTBF": "Mean Time Between Failure",
    "MTTR": "Mean Time To Repair",
    "MTU": "Maximum Transmission Unit",
    "MX": "Mail Exchange",
    "NAC": "Network Access Control",
    "NAS": "Network-attached Storage",
    "NAT": "Network Address Translation",
    "NFV": "Network Functions Virtualization",
    "NIC": "Network Interface Card",
    "NS": "Name Server",
    "NTP": "Network Time Protocol",
    "NTS": "Network Time Security",
    "OS": "Operating System",
    "OSPF": "Open Shortest Path First",
    "OSI": "Open Systems Interconnection",
    "OT": "Operational Technology",
    "PaaS": "Platform as a Service",
    "PAT": "Port Address Translation",
    "PCI DSS": "Payment Card Industry Data Security Standards",
    "PDU": "Power Distribution Unit",
    "PKI": "Public Key Infrastructure",
    "PoE": "Power over Ethernet",
    "PSK": "Pre-shared Key",
    "PTP": "Precision Time Protocol",
    "PTR": "Pointer",
    "QoS": "Quality of Service",
    "QSFP": "Quad Small Form-factor Pluggable",
    "RADIUS": "Remote Authentication Dial-in User Service",
    "RDP": "Remote Desktop Protocol",
    "RFID": "Radio Frequency Identifier",
    "RIP": "Routing Information Protocol",
    "RJ": "Registered Jack",
    "RPO": "Recovery Point Objective",
    "RSTP": "Rapid Spanning Tree Protocol",
    "RTO": "Recovery Time Objective",
    "RX": "Receiver",
    "SaaS": "Software as a Service",
    "SAML": "Security Assertion Markup Language",
    "SAN": "Storage Area Network",
    "SASE": "Secure Access Service Edge",
    "SC": "Subscriber Connector",
    "SCADA": "Supervisory Control and Data Acquisition",
    "SDN": "Software-defined Network",
    "SD-WAN": "Software-defined Wide Area Network",
    "SFP": "Small Form-factor Pluggable",
    "SFTP": "Secure File Transfer Protocol",
    "SIP": "Session Initiation Protocol",
    "SIEM": "Security Information and Event Management",
    "SLA": "Service-level Agreement",
    "SLAAC": "Stateless Address Autoconfiguration",
    "SMB": "Server Message Block",
    "SMTP": "Simple Mail Transfer Protocol",
    "SMTPS": "Simple Mail Transfer Protocol Secure",
    "SNMP": "Simple Network Management Protocol",
    "SOA": "Start of Authority",
    "SQL": "Structured Query Language",
    "SSE": "Security Service Edge",
    "SSH": "Secure Shell",
    "SSID": "Service Set Identifier",
    "SSL": "Secure Socket Layer",
    "SSO": "Single Sign-on",
    "ST": "Straight Tip",
    "STP": "Shielded Twisted Pair",
    "SVI": "Switch Virtual Interface",
    "TACACS+": "Terminal Access Controller Access Control System Plus",
    "TCP": "Transmission Control Protocol",
    "TFTP": "Trivial File Transfer Protocol",
    "TTL": "Time to Live",
    "TX": "Transmitter",
    "TXT": "Text",
    "UDP": "User Datagram Protocol",
    "UPS": "Uninterruptible Power Supply",
    "URL": "Uniform Resource Locator",
    "USB": "Universal Serial Bus",
    "UTM": "Unified Threat Management",
    "UTP": "Unshielded Twisted Pair",
    "VIP": "Virtual IP",
    "VLAN": "Virtual Local Area Network",
    "VLSM": "Variable Length Subnet Mask",
    "VoIP": "Voice over IP",
    "VPC": "Virtual Private Cloud",
    "VPN": "Virtual Private Network",
    "WAN": "Wide Area Network",
    "WPA": "Wi-Fi Protected Access",
    "WPS": "Wi-Fi Protected Setup",
    "VXLAN": "Virtual Extensible LAN",
    "ZTA": "Zero Trust Architecture",
}


def _acronym_rounds(items):
    score, asked = 0, 0
    try:
        for n, (abbr, full) in enumerate(items, 1):
            print()
            print(wrap(f"{n}. {C.BOLD}{abbr}{C.RESET} stands for...?"))
            ans = normalize(get_input("  Expansion: "))
            target = normalize(full)
            ratio = difflib.SequenceMatcher(None, ans, target).ratio()
            asked += 1
            if ratio >= 0.82:
                score += 1
                print(C.GREEN + C.BOLD + "  ✔ Correct!" + C.RESET +
                      C.DIM + f"  ({full})" + C.RESET)
            elif ratio >= 0.55 and ans:
                print(C.YELLOW + f"  Close. Official: {full}" + C.RESET)
                g = get_input("  Count it? (y/n): ").lower()
                if g.startswith("y"):
                    score += 1
            else:
                print(C.RED + C.BOLD + f"  ✘ {abbr} = {full}" + C.RESET)
    except QuitRound:
        pass
    if asked:
        print()
        print(grade_line(score, asked))


def acronym_blitz():
    banner("ACRONYM BLITZ", C.MAGENTA)
    total = len(ACRONYMS)
    print(wrap(f"The official N10-009 acronym list has {total} entries and "
               "CompTIA expects you to know all of them. Type the expansion; "
               "close answers are auto-judged, borderline ones you self-grade. "
               "q to stop."))
    quarter = -(-total // 4)
    print()
    print(f"  1) Full stack  — all {total} acronyms in one run")
    print(f"  2) Quarter set — one 25% set (~{quarter} acronyms) at a time")
    try:
        mode = get_input("  Choose 1 or 2 (q to cancel): ")
    except QuitRound:
        return
    items = sorted(ACRONYMS.items())
    if mode == "2":
        sets = [items[i:i + quarter] for i in range(0, total, quarter)]
        print()
        for i, chunk in enumerate(sets, 1):
            print(f"    {i}) Set {i}  ({len(chunk)} acronyms)")
        try:
            pick = get_input(f"  Which set (1-{len(sets)})? ")
        except QuitRound:
            return
        if not (pick.isdigit() and 1 <= int(pick) <= len(sets)):
            print(C.YELLOW + "  Not a valid set — cancelled." + C.RESET)
            return
        items = list(sets[int(pick) - 1])
    random.shuffle(items)
    _acronym_rounds(items)


# -------------------------------------------------------------- subnetting ---

def _rand_ip_network(min_prefix, max_prefix):
    prefix = random.randint(min_prefix, max_prefix)
    ip = ipaddress.IPv4Address(random.randint(0x0A000001, 0xDF000000))
    net = ipaddress.ip_network(f"{ip}/{prefix}", strict=False)
    return ip, net


def _mask_math(net):
    """Explain the magic-number method for this network."""
    prefix = net.prefixlen
    mask = str(net.netmask)
    octets = [int(o) for o in mask.split(".")]
    idx = next((i for i, o in enumerate(octets) if o != 255), 3)
    block = 256 - octets[idx]
    return (f"Mask /{prefix} = {mask}. Interesting octet #{idx + 1} "
            f"(value {octets[idx]}), block size = 256 - {octets[idx]} = {block}. "
            f"Networks increment by {block} in that octet.")


def _ask_ip(prompt, expected):
    ans = get_input(prompt)
    try:
        return ipaddress.ip_address(ans.strip()) == expected
    except ValueError:
        return False


def _ask_int(prompt, expected):
    ans = get_input(prompt).replace(",", "").strip()
    try:
        return int(ans) == expected
    except ValueError:
        return False


def _subnet_question(level):
    """Returns (asker() -> (bool, explanation_str))."""
    kinds = {
        1: ["cidr2mask", "mask2cidr", "hosts", "identify"],
        2: ["network", "broadcast", "first", "last", "hosts", "same"],
        3: ["fit", "count_subnets", "same", "network", "design"],
    }[level]
    kind = random.choice(kinds)

    if kind == "cidr2mask":
        p = random.randint(8, 30)
        net = ipaddress.ip_network(f"10.0.0.0/{p}", strict=False)
        expected = str(net.netmask)

        def go():
            print(wrap(f"Convert /{p} to a dotted-decimal subnet mask."))
            ok = normalize(get_input("  Mask: ")) == normalize(expected)
            return ok, f"/{p} = {expected}."
        return go

    if kind == "mask2cidr":
        p = random.randint(8, 30)
        mask = str(ipaddress.ip_network(f"10.0.0.0/{p}", strict=False).netmask)

        def go():
            print(wrap(f"Convert {mask} to CIDR prefix notation."))
            ans = get_input("  Prefix (e.g. /24): ").lstrip("/")
            ok = ans.strip() == str(p)
            return ok, f"{mask} = /{p}."
        return go

    if kind == "identify":
        choices = [
            ("10.{}.{}.{}".format(random.randint(0, 255), random.randint(0, 255),
                                  random.randint(1, 254)), "private", "RFC1918 10.0.0.0/8"),
            ("172.{}.{}.{}".format(random.randint(16, 31), random.randint(0, 255),
                                   random.randint(1, 254)), "private", "RFC1918 172.16.0.0/12"),
            ("192.168.{}.{}".format(random.randint(0, 255), random.randint(1, 254)),
             "private", "RFC1918 192.168.0.0/16"),
            ("169.254.{}.{}".format(random.randint(0, 255), random.randint(1, 254)),
             "apipa", "APIPA/link-local 169.254.0.0/16 - means DHCP failed"),
            ("127.0.0.1", "loopback", "Loopback 127.0.0.0/8 - localhost"),
            ("8.8.8.8", "public", "Publicly routable address"),
            ("203.0.{}.{}".format(random.randint(0, 255), random.randint(1, 254)),
             "public", "Publicly routable address"),
        ]
        ip, answer, why = random.choice(choices)
        accepted = {
            "private": ["private", "rfc1918", "private ip"],
            "public": ["public", "public ip", "routable"],
            "apipa": ["apipa", "link local", "automatic private"],
            "loopback": ["loopback", "localhost"],
        }[answer]

        def go():
            print(wrap(f"Classify this address: {ip}  "
                       "(public / private / APIPA / loopback)"))
            ok = normalize(get_input("  Type: ")) in [normalize(a) for a in accepted]
            return ok, why
        return go

    if kind == "hosts":
        p = random.randint(8, 30)
        expected = 2 ** (32 - p) - 2

        def go():
            print(wrap(f"How many USABLE host addresses are in a /{p} network?"))
            ok = _ask_int("  Hosts: ", expected)
            return ok, (f"Host bits = 32 - {p} = {32 - p}; usable = 2^{32 - p} - 2 "
                        f"= {expected} (subtract network and broadcast).")
        return go

    if kind in ("network", "broadcast", "first", "last"):
        ip, net = _rand_ip_network(16, 29)
        target = {
            "network": net.network_address,
            "broadcast": net.broadcast_address,
            "first": net.network_address + 1,
            "last": net.broadcast_address - 1,
        }[kind]
        label = {"network": "network address", "broadcast": "broadcast address",
                 "first": "FIRST usable host", "last": "LAST usable host"}[kind]

        def go():
            print(wrap(f"For the host {ip}/{net.prefixlen}, what is the {label}?"))
            ok = _ask_ip("  Address: ", target)
            return ok, (f"{label.capitalize()} = {target}. Network {net.network_address} "
                        f"- broadcast {net.broadcast_address}. " + _mask_math(net))
        return go

    if kind == "same":
        _, net = _rand_ip_network(20, 28)
        a = net.network_address + random.randint(1, max(1, net.num_addresses - 2))
        if random.random() < 0.5:
            b = net.network_address + random.randint(1, max(1, net.num_addresses - 2))
        else:
            other = ipaddress.ip_network(
                (int(net.network_address) + net.num_addresses, net.prefixlen))
            b = other.network_address + random.randint(1, max(1, other.num_addresses - 2))
        same = ipaddress.ip_network(f"{a}/{net.prefixlen}", strict=False) == \
            ipaddress.ip_network(f"{b}/{net.prefixlen}", strict=False)

        def go():
            print(wrap(f"Are {a} and {b} on the SAME subnet, given mask /{net.prefixlen}? (y/n)"))
            ans = get_input("  y/n: ").lower()
            ok = ans.startswith("y") == same
            na = ipaddress.ip_network(f"{a}/{net.prefixlen}", strict=False)
            nb = ipaddress.ip_network(f"{b}/{net.prefixlen}", strict=False)
            return ok, (f"{a} is in {na}; {b} is in {nb} - "
                        f"{'same' if same else 'different'} subnet(s). " + _mask_math(net))
        return go

    if kind == "fit" or kind == "design":
        hosts = random.choice([2, 5, 10, 25, 30, 60, 100, 120, 250, 500, 1000])
        p = 32
        while 2 ** (32 - p) - 2 < hosts:
            p -= 1

        def go():
            print(wrap(f"A subnet must support {hosts} hosts. What is the SMALLEST "
                       "subnet (longest prefix) that works?"))
            ans = get_input("  Prefix (e.g. /26): ").lstrip("/")
            ok = ans.strip() == str(p)
            return ok, (f"/{p} gives 2^{32 - p} - 2 = {2 ** (32 - p) - 2} usable hosts, "
                        f"the smallest block that fits {hosts}. One prefix longer "
                        f"(/{p + 1}) only allows {2 ** (31 - p) - 2}.")
        return go

    if kind == "count_subnets":
        big = random.randint(16, 24)
        small = big + random.randint(1, 6)
        expected = 2 ** (small - big)

        def go():
            print(wrap(f"How many /{small} subnets fit inside one /{big}?"))
            ok = _ask_int("  Count: ", expected)
            return ok, f"2^({small} - {big}) = {expected} subnets."
        return go


def subnet_drill():
    banner("SUBNETTING GYM", C.MAGENTA)
    print("""
  1) Level 1 - Basics      (mask conversion, host counts, address types)
  2) Level 2 - Subnetting  (network/broadcast/usable range)
  3) Level 3 - Design      (VLSM sizing, subnet counts)
""")
    score, asked = 0, 0
    try:
        while True:
            lvl = get_input("  Level (1-3): ")
            if lvl in ("1", "2", "3"):
                break
        level = int(lvl)
        print(wrap("Problems are randomly generated - infinite practice. "
                   "Type q to stop."))
        while True:
            print()
            print(C.BLUE + C.BOLD + f"--- Problem {asked + 1} " + "-" * 50 + C.RESET)
            go = _subnet_question(level)
            ok, explanation = go()
            asked += 1
            if ok:
                score += 1
                print(C.GREEN + C.BOLD + "  ✔ Correct!" + C.RESET)
            else:
                print(C.RED + C.BOLD + "  ✘ Incorrect." + C.RESET)
            print(C.DIM + wrap("» " + explanation, indent=2) + C.RESET)
    except QuitRound:
        pass
    if asked:
        print()
        print(grade_line(score, asked))
