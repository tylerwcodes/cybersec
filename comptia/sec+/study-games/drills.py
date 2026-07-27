"""Special drills: control classifier gym, port & protocol blitz, acronym blitz.

The control categories/types, protocol list, and acronym list follow the
official SY0-701 exam objectives document.
"""
import difflib
import random

from engine import (C, QuitRound, banner, get_input, grade_line, normalize,
                    wrap)

# ---------------------------------------------------------------- controls ---
# SY0-701 objective 1.1 — categories and types of security controls.
CATEGORIES = {
    "technical": ["technical", "logical", "technical control"],
    "managerial": ["managerial", "management", "administrative", "managerial control"],
    "operational": ["operational", "operations", "operational control"],
    "physical": ["physical", "physical control"],
}
TYPES = {
    "preventive": ["preventive", "preventative", "prevention", "prevent"],
    "deterrent": ["deterrent", "deterrence", "deter"],
    "detective": ["detective", "detection", "detect"],
    "corrective": ["corrective", "correction", "correct", "recovery"],
    "compensating": ["compensating", "compensatory", "compensation", "compensating control"],
    "directive": ["directive", "direction", "direct"],
}

# (scenario, category, type, ask, explanation)
# ask: "c" = only ask category, "t" = only ask type, "ct" = either
CONTROLS = [
    ("A firewall rule blocks all inbound connections on unused ports.",
     "technical", "preventive", "ct",
     "Enforced by a device/software = technical; it stops the event before it happens = preventive."),
    ("Full-disk encryption protects the drives of all company laptops.",
     "technical", "preventive", "ct",
     "Encryption is enforced electronically (technical) and prevents disclosure if a laptop is stolen (preventive)."),
    ("Multifactor authentication is required for every VPN login.",
     "technical", "preventive", "ct",
     "MFA is enforced by the system (technical) and blocks unauthorized access before it occurs (preventive)."),
    ("A SIEM raises an alert when a user logs in from two countries an hour apart.",
     "technical", "detective", "ct",
     "The SIEM is software (technical) that identifies suspicious activity as/after it happens (detective) — impossible travel is a classic indicator."),
    ("An IDS flags traffic matching the signature of a known exploit.",
     "technical", "detective", "ct",
     "An IDS only detects and reports (detective); an IPS would also block (preventive). Both are technical controls."),
    ("Antivirus software quarantines a malicious file it discovered on a workstation.",
     "technical", "corrective", "ct",
     "Quarantine/removal fixes a problem that already occurred, making it corrective; antivirus is a technical control."),
    ("Backup software automatically restores files corrupted by ransomware.",
     "technical", "corrective", "ct",
     "Restoring from backup reverses damage after an incident — the textbook corrective control, implemented technically."),
    ("A login banner warns that all activity is monitored and violators will be prosecuted.",
     "technical", "deterrent", "t",
     "The banner doesn't stop anyone technically — it discourages misuse through fear of consequences (deterrent). (Its category is debatable — displayed by the system, but really a policy statement — so this drill only asks for the type.)"),
    ("A legacy server that cannot be patched is isolated on its own firewalled VLAN segment.",
     "technical", "compensating", "ct",
     "Segmentation stands in for the unavailable primary control (patching) — a compensating control, implemented technically."),
    ("An account lockout policy disables an account after five failed password attempts.",
     "technical", "preventive", "ct",
     "Lockout is enforced by the system (technical) and prevents further brute-force guessing (preventive)."),
    ("A hiring policy requires background checks before anyone is granted system access.",
     "managerial", "preventive", "ct",
     "Policies and management decisions are managerial; screening people before granting access prevents incidents."),
    ("The acceptable use policy (AUP) tells employees how company systems may be used.",
     "managerial", "directive", "ct",
     "An AUP is a management document (managerial) whose purpose is to direct behavior — the hallmark of a directive control."),
    ("A standard operating procedure directs analysts to verify hashes before installing software.",
     "managerial", "directive", "ct",
     "SOPs are documented management controls that tell people what to do — directive."),
    ("Management reviews quarterly audit reports of user access rights.",
     "managerial", "detective", "ct",
     "Audits and reviews discover problems after the fact (detective) and are a management activity (managerial)."),
    ("A risk assessment is performed before the company adopts a new cloud service.",
     "managerial", "preventive", "c",
     "Risk assessments are managerial controls — management processes that shape security decisions before problems occur."),
    ("Company policy states that employees who violate security rules will be dismissed.",
     "managerial", "deterrent", "ct",
     "The threat of dismissal discourages violations (deterrent) and is set by policy (managerial)."),
    ("After a breach, the security team updates policies based on lessons learned.",
     "managerial", "corrective", "ct",
     "Fixing the control environment after an incident is corrective; policy work is managerial."),
    ("Until the new IAM platform is deployed, a policy requires manager sign-off for every privileged account request.",
     "managerial", "compensating", "ct",
     "A temporary alternative standing in for a control that isn't available yet = compensating; it is enforced through policy (managerial)."),
    ("A security guard checks employee badges at the building entrance.",
     "operational", "preventive", "ct",
     "Controls executed by people day-to-day are operational; stopping unauthorized entry before it happens is preventive."),
    ("A guard reviews the visitor log every morning looking for anomalies.",
     "operational", "detective", "ct",
     "Log review by a person is operational, and reviewing records to discover issues after the fact is detective."),
    ("A visible security guard posted in the lobby discourages tailgating attempts.",
     "operational", "deterrent", "ct",
     "The guard's visible presence discourages the attempt (deterrent); guards are people-executed, so operational."),
    ("While the badge reader is broken, a guard manually checks IDs at the door.",
     "operational", "compensating", "ct",
     "A person standing in for a failed primary control is the classic compensating example; performed by people = operational."),
    ("The incident response team follows its runbook to contain and eradicate an infection.",
     "operational", "corrective", "ct",
     "IR activities are performed by people (operational) and fix/limit damage after an incident (corrective)."),
    ("New employees must complete security awareness training during onboarding.",
     "operational", "directive", "c",
     "Training is carried out by/for people (operational); it directs users toward correct behavior."),
    ("A change advisory board must approve firewall changes before implementation.",
     "managerial", "preventive", "c",
     "Change management approval is a management process (managerial) intended to prevent risky, unauthorized changes."),
    ("Bollards in front of the lobby prevent vehicles from driving into the entrance.",
     "physical", "preventive", "ct",
     "Bollards are a tangible barrier (physical) that stops the event outright (preventive)."),
    ("An access control vestibule allows only one authenticated person through at a time.",
     "physical", "preventive", "ct",
     "The vestibule (mantrap) physically blocks tailgating — physical category, preventive type."),
    ("CCTV cameras record everyone entering the data center.",
     "physical", "detective", "ct",
     "Cameras don't physically stop entry; they capture evidence and reveal what happened (detective). Video surveillance is classed as a physical security control."),
    ("Warning signs on the perimeter fence state the area is under video surveillance.",
     "physical", "deterrent", "ct",
     "Signs change attacker behavior through perceived risk (deterrent) and are part of the physical environment."),
    ("A fire suppression system extinguishes a fire in the server room.",
     "physical", "corrective", "ct",
     "It acts after the fire starts to limit/repair damage (corrective) and protects the physical facility."),
    ("A sign on the server-room door reads 'Authorized Personnel Only'.",
     "physical", "directive", "ct",
     "The sign directs behavior rather than enforcing it — directive, in the physical environment."),
    ("A backup generator keeps systems running during a power outage.",
     "physical", "compensating", "ct",
     "The generator substitutes for the failed primary power source — compensating, and it's physical infrastructure."),
    ("Server-room doors use biometric locks to admit only cleared engineers.",
     "physical", "preventive", "ct",
     "Locks physically restrict access (physical, preventive). Compare: the *policy* deciding who is cleared would be managerial."),
    ("Motion sensors in the warehouse alert security when movement is detected after hours.",
     "physical", "detective", "ct",
     "Sensors (infrared, pressure, microwave, ultrasonic) detect and report intrusions — detective controls in the physical space."),
    ("An IPS inline on the network edge drops packets that match attack signatures.",
     "technical", "preventive", "ct",
     "Unlike an IDS (detective), an IPS sits inline and blocks the attack before it reaches the target — preventive and technical."),
    ("Security staff perform daily log reviews of privileged account activity.",
     "operational", "detective", "ct",
     "People reviewing logs day-to-day = operational; discovering misuse after the fact = detective."),
]


def control_gym():
    banner("CONTROL CLASSIFIER GYM", C.MAGENTA)
    print(wrap("Objective 1.1 hands you a control and expects an instant "
               "classification. Categories: technical, managerial, operational, "
               "physical. Types: preventive, deterrent, detective, corrective, "
               "compensating, directive. Type q to stop."))
    score, asked = 0, 0
    pool = []
    try:
        while True:
            if not pool:
                pool = list(CONTROLS)
                random.shuffle(pool)
            scenario, cat, typ, ask, why = pool.pop()
            dim = random.choice([d for d in ask])
            print()
            print(C.BLUE + C.BOLD + f"--- Control {asked + 1} " + "-" * 50 + C.RESET)
            print(wrap(scenario))
            if dim == "c":
                print(wrap("  Category? (technical / managerial / operational / physical)", indent=2))
                ans = normalize(get_input("  Category: "))
                ok = ans in [normalize(a) for a in CATEGORIES[cat]]
                right = cat
            else:
                print(wrap("  Type? (preventive / deterrent / detective / corrective / "
                           "compensating / directive)", indent=2))
                ans = normalize(get_input("  Type: "))
                ok = ans in [normalize(a) for a in TYPES[typ]]
                right = typ
            asked += 1
            if ok:
                score += 1
                print(C.GREEN + C.BOLD + "  ✔ Correct!" + C.RESET)
            else:
                print(C.RED + C.BOLD + f"  ✘ It's {right} ({cat}/{typ})." + C.RESET)
            print(C.DIM + wrap("» " + why, indent=2) + C.RESET)
    except QuitRound:
        pass
    if asked:
        print()
        print(grade_line(score, asked))


# ------------------------------------------------------------------- ports ---
# (name, abbreviation, display port, acceptable answers, transport/notes)
PORTS = [
    ("File Transfer Protocol", "FTP", "20/21",
     ["20 21", "21 20", "21", "20"], "TCP - cleartext; replace with SFTP (22) or FTPS (990)"),
    ("Secure Shell", "SSH", "22",
     ["22"], "TCP - encrypted remote CLI; replaces Telnet"),
    ("SSH File Transfer Protocol", "SFTP", "22",
     ["22"], "TCP - file transfer tunneled over SSH"),
    ("Telnet", "Telnet", "23",
     ["23"], "TCP - legacy plaintext remote CLI; replace with SSH"),
    ("Simple Mail Transfer Protocol", "SMTP", "25",
     ["25"], "TCP - cleartext mail relay between servers"),
    ("Terminal Access Controller Access Control System Plus", "TACACS+", "49",
     ["49"], "TCP - AAA for device administration; encrypts entire payload"),
    ("Domain Name System", "DNS", "53",
     ["53"], "UDP queries / TCP zone transfers; secure with DNSSEC, DoT (853), DoH (443)"),
    ("Dynamic Host Configuration Protocol", "DHCP", "67/68",
     ["67 68", "68 67", "67", "68"], "UDP - 67 server, 68 client"),
    ("Hypertext Transfer Protocol", "HTTP", "80",
     ["80"], "TCP - unencrypted web; replace with HTTPS (443)"),
    ("Kerberos", "Kerberos", "88",
     ["88"], "TCP/UDP - ticket-based authentication in Windows domains"),
    ("Post Office Protocol v3", "POP3", "110",
     ["110"], "TCP - cleartext mail retrieval; secure version POP3S (995)"),
    ("Network Time Protocol", "NTP", "123",
     ["123"], "UDP - time synchronization (accurate logs, Kerberos, TOTP)"),
    ("Internet Message Access Protocol", "IMAP", "143",
     ["143"], "TCP - cleartext mailbox access; secure version IMAPS (993)"),
    ("Simple Network Management Protocol", "SNMP", "161/162",
     ["161 162", "162 161", "161", "162"], "UDP - 161 queries, 162 traps; only v3 adds encryption"),
    ("Lightweight Directory Access Protocol", "LDAP", "389",
     ["389"], "TCP/UDP - directory services; secure with LDAPS (636)"),
    ("Hypertext Transfer Protocol Secure", "HTTPS", "443",
     ["443"], "TCP - web over TLS"),
    ("Server Message Block", "SMB", "445",
     ["445"], "TCP - Windows file/printer sharing; block at the perimeter"),
    ("Internet Key Exchange (IPSec)", "IKE", "500",
     ["500"], "UDP - negotiates IPSec VPN tunnels; NAT-T uses 4500"),
    ("Syslog", "Syslog", "514",
     ["514"], "UDP - cleartext log forwarding; secure version uses TLS on 6514"),
    ("Simple Mail Transfer Protocol Secure", "SMTPS", "465/587",
     ["465 587", "587 465", "587", "465"], "TCP - 587 submission with STARTTLS, 465 implicit TLS"),
    ("Lightweight Directory Access Protocol Secure", "LDAPS", "636",
     ["636"], "TCP - LDAP over SSL/TLS"),
    ("Layer 2 Tunneling Protocol", "L2TP", "1701",
     ["1701"], "UDP - VPN tunneling; no native encryption, pair with IPSec"),
    ("Structured Query Language (SQL) Server", "SQL Server", "1433",
     ["1433"], "TCP - Microsoft SQL Server database"),
    ("Remote Authentication Dial-In User Service", "RADIUS", "1812/1813",
     ["1812 1813", "1813 1812", "1812", "1813"], "UDP - 1812 authentication, 1813 accounting; encrypts only the password"),
    ("Remote Desktop Protocol", "RDP", "3389",
     ["3389"], "TCP - graphical remote desktop; brute-force magnet, gate behind VPN/MFA"),
    ("Session Initiation Protocol", "SIP", "5060/5061",
     ["5060 5061", "5061 5060", "5060", "5061"], "TCP/UDP - VoIP call setup; 5061 is TLS-secured"),
    ("Syslog over TLS", "Syslog-TLS", "6514",
     ["6514"], "TCP - encrypted syslog forwarding"),
    ("Internet Message Access Protocol Secure", "IMAPS", "993",
     ["993"], "TCP - IMAP over TLS"),
    ("Post Office Protocol v3 Secure", "POP3S", "995",
     ["995"], "TCP - POP3 over TLS"),
]

# (insecure protocol/technology, accepted secure replacements, explanation)
SWAPS = [
    ("Telnet", ["ssh", "secure shell"],
     "SSH (TCP 22) provides an encrypted remote CLI; Telnet (23) sends everything, including credentials, in cleartext."),
    ("HTTP", ["https", "hypertext transfer protocol secure", "http over tls", "tls"],
     "HTTPS wraps HTTP in TLS on port 443, protecting confidentiality and integrity of web traffic."),
    ("FTP", ["sftp", "ftps", "secure file transfer protocol", "ssh file transfer protocol", "ftp secure"],
     "SFTP (SSH, port 22) or FTPS (TLS, 989/990) — both encrypt file transfers that FTP sends in cleartext."),
    ("SNMPv2c", ["snmpv3", "snmp v3", "snmp version 3"],
     "Only SNMPv3 adds authentication and encryption; v1/v2c use cleartext community strings."),
    ("LDAP", ["ldaps", "ldap over ssl", "ldap over tls", "lightweight directory access protocol secure", "secure ldap"],
     "LDAPS (TCP 636) encrypts directory queries and bind credentials that plain LDAP (389) exposes."),
    ("POP3", ["pop3s", "secure pop3", "pop3 over tls", "pop3 over ssl"],
     "POP3S (TCP 995) is POP3 wrapped in TLS; plain POP3 (110) sends passwords in cleartext."),
    ("IMAP", ["imaps", "secure imap", "imap over tls", "imap over ssl"],
     "IMAPS (TCP 993) is IMAP wrapped in TLS; plain IMAP (143) is cleartext."),
    ("SMTP (cleartext relay)", ["smtps", "smtp with starttls", "starttls", "smtp over tls", "secure smtp"],
     "SMTPS/STARTTLS on 587 (legacy implicit TLS 465) encrypts mail submission; port 25 SMTP is cleartext."),
    ("DNS", ["dnssec", "dns over tls", "dot", "dns over https", "doh"],
     "DNSSEC signs records (integrity/origin authentication); DoT (853) and DoH (443) encrypt the queries themselves."),
    ("RTP (voice/video streams)", ["srtp", "secure real time transport protocol", "secure rtp"],
     "SRTP (typically UDP 5004) adds encryption and integrity to voice/video media streams."),
    ("Syslog over UDP 514", ["syslog over tls", "syslog tls", "secure syslog", "6514", "syslog over tcp with tls"],
     "Forward logs with TLS on TCP 6514 so log data can't be read or tampered with in transit."),
    ("WEP or WPA (wireless)", ["wpa3", "wpa2", "wpa2 aes", "wpa3 sae"],
     "WPA3 (SAE handshake) is the current standard; WPA2-AES is the minimum acceptable. WEP and original WPA/TKIP are broken."),
    ("SSL", ["tls", "transport layer security"],
     "All SSL versions are deprecated and vulnerable (e.g., POODLE); modern systems should require TLS 1.2+."),
    ("Unencrypted email content", ["s mime", "smime", "secure multipurpose internet mail extensions", "pgp", "gpg"],
     "S/MIME (certificate-based) or PGP/GPG encrypt and/or sign the message body end to end."),
]


def port_blitz(rounds=15):
    banner("PORT & PROTOCOL BLITZ", C.MAGENTA)
    print(wrap("Sec+ expects the common port table AND the secure replacement "
               "for every insecure protocol (objective 4.5). Forward, reverse, "
               "and secure-swap questions, streak bonuses shown. Type q to stop."))
    score, streak, best_streak = 0, 0, 0
    asked = 0
    try:
        for n in range(1, rounds + 1):
            mode = random.random()
            print()
            if mode < 0.35:
                name, abbr, port, accepted, notes = random.choice(PORTS)
                print(wrap(f"{n}. What port(s) does {C.BOLD}{name} ({abbr}){C.RESET} use?"))
                ans = normalize(get_input("  Port(s): "))
                ok = ans in [normalize(a) for a in accepted]
                miss = f"{abbr} = port {port}"
                note = f"{abbr}: {notes}"
            elif mode < 0.7:
                name, abbr, port, accepted, notes = random.choice(PORTS)
                print(wrap(f"{n}. Which protocol uses port {C.BOLD}{port}{C.RESET}?"))
                ans = normalize(get_input("  Protocol: "))
                # any protocol sharing that display port counts (SSH/SFTP on 22)
                valid = [p for p in PORTS if p[2] == port]
                names = [normalize(p[0]) for p in valid] + [normalize(p[1]) for p in valid]
                ok = ans in names
                miss = f"{abbr} = port {port}"
                note = f"{abbr}: {notes}"
            else:
                insecure, accepted, why = random.choice(SWAPS)
                print(wrap(f"{n}. What is the SECURE replacement for {C.BOLD}{insecure}{C.RESET}?"))
                ans = normalize(get_input("  Secure version: "))
                ok = ans in [normalize(a) for a in accepted]
                miss = f"{insecure} → {accepted[0].upper()}"
                note = why
            asked += 1
            if ok:
                score += 1
                streak += 1
                best_streak = max(best_streak, streak)
                flame = " 🔥" * min(3, streak // 3)
                print(C.GREEN + C.BOLD + f"  ✔ Correct! (streak {streak}){flame}" + C.RESET)
            else:
                streak = 0
                print(C.RED + C.BOLD + f"  ✘ {miss}" + C.RESET)
            print(C.DIM + wrap(note, indent=4) + C.RESET)
    except QuitRound:
        pass
    if asked:
        print()
        print(grade_line(score, asked))
        print(C.DIM + f"  Best streak: {best_streak}" + C.RESET)


# ---------------------------------------------------------------- acronyms ---
# Official SY0-701 acronym list (objectives document). Multi-meaning entries
# are separated with " / " — any one meaning counts as correct.
ACRONYMS = {
    "AAA": "Authentication, Authorization, and Accounting",
    "ACL": "Access Control List",
    "AES": "Advanced Encryption Standard",
    "AH": "Authentication Header",
    "AI": "Artificial Intelligence",
    "AIS": "Automated Indicator Sharing",
    "ALE": "Annualized Loss Expectancy",
    "AP": "Access Point",
    "API": "Application Programming Interface",
    "APT": "Advanced Persistent Threat",
    "ARO": "Annualized Rate of Occurrence",
    "ARP": "Address Resolution Protocol",
    "ASLR": "Address Space Layout Randomization",
    "AUP": "Acceptable Use Policy",
    "AV": "Antivirus",
    "BCP": "Business Continuity Planning",
    "BGP": "Border Gateway Protocol",
    "BIA": "Business Impact Analysis",
    "BIOS": "Basic Input/Output System",
    "BPA": "Business Partners Agreement",
    "BPDU": "Bridge Protocol Data Unit",
    "BYOD": "Bring Your Own Device",
    "CA": "Certificate Authority",
    "CAPTCHA": "Completely Automated Public Turing Test to Tell Computers and Humans Apart",
    "CASB": "Cloud Access Security Broker",
    "CBC": "Cipher Block Chaining",
    "CCMP": "Counter Mode/CBC-MAC Protocol",
    "CCTV": "Closed-Circuit Television",
    "CERT": "Computer Emergency Response Team",
    "CHAP": "Challenge Handshake Authentication Protocol",
    "CIA": "Confidentiality, Integrity, and Availability",
    "CIO": "Chief Information Officer",
    "CIRT": "Computer Incident Response Team",
    "COOP": "Continuity of Operation Planning",
    "COPE": "Corporate Owned, Personally Enabled",
    "CRC": "Cyclic Redundancy Check",
    "CRL": "Certificate Revocation List",
    "CSO": "Chief Security Officer",
    "CSP": "Cloud Service Provider",
    "CSR": "Certificate Signing Request",
    "CSRF": "Cross-Site Request Forgery",
    "CTO": "Chief Technology Officer",
    "CVE": "Common Vulnerabilities and Exposures",
    "CVSS": "Common Vulnerability Scoring System",
    "CYOD": "Choose Your Own Device",
    "DAC": "Discretionary Access Control",
    "DBA": "Database Administrator",
    "DDoS": "Distributed Denial-of-Service",
    "DEP": "Data Execution Prevention",
    "DES": "Data Encryption Standard",
    "DHCP": "Dynamic Host Configuration Protocol",
    "DHE": "Diffie-Hellman Ephemeral",
    "DKIM": "DomainKeys Identified Mail",
    "DLL": "Dynamic Link Library",
    "DLP": "Data Loss Prevention",
    "DMARC": "Domain-based Message Authentication, Reporting, and Conformance",
    "DNAT": "Destination Network Address Translation",
    "DNS": "Domain Name System",
    "DoS": "Denial-of-Service",
    "DPO": "Data Privacy Officer",
    "DRP": "Disaster Recovery Plan",
    "DSA": "Digital Signature Algorithm",
    "EAP": "Extensible Authentication Protocol",
    "ECB": "Electronic Code Book",
    "ECC": "Elliptic Curve Cryptography",
    "ECDHE": "Elliptic Curve Diffie-Hellman Ephemeral",
    "ECDSA": "Elliptic Curve Digital Signature Algorithm",
    "EDR": "Endpoint Detection and Response",
    "EFS": "Encrypting File System",
    "ERP": "Enterprise Resource Planning",
    "ESP": "Encapsulating Security Payload",
    "FDE": "Full-Disk Encryption",
    "FIM": "File Integrity Monitoring",
    "FPGA": "Field-Programmable Gate Array",
    "FRR": "False Rejection Rate",
    "FTP": "File Transfer Protocol",
    "FTPS": "File Transfer Protocol Secure",
    "GCM": "Galois/Counter Mode",
    "GDPR": "General Data Protection Regulation",
    "GPG": "GNU Privacy Guard",
    "GPO": "Group Policy Object",
    "GPS": "Global Positioning System",
    "GPU": "Graphics Processing Unit",
    "GRE": "Generic Routing Encapsulation",
    "HA": "High Availability",
    "HDD": "Hard Disk Drive",
    "HIDS": "Host-based Intrusion Detection System",
    "HIPS": "Host-based Intrusion Prevention System",
    "HMAC": "Hash-based Message Authentication Code",
    "HOTP": "HMAC-based One-Time Password",
    "HSM": "Hardware Security Module",
    "HTML": "Hypertext Markup Language",
    "HTTP": "Hypertext Transfer Protocol",
    "HTTPS": "Hypertext Transfer Protocol Secure",
    "HVAC": "Heating, Ventilation, and Air Conditioning",
    "IaaS": "Infrastructure as a Service",
    "IaC": "Infrastructure as Code",
    "IAM": "Identity and Access Management",
    "ICMP": "Internet Control Message Protocol",
    "ICS": "Industrial Control Systems",
    "IdP": "Identity Provider",
    "IDS": "Intrusion Detection System",
    "IEEE": "Institute of Electrical and Electronics Engineers",
    "IKE": "Internet Key Exchange",
    "IM": "Instant Messaging",
    "IMAP": "Internet Message Access Protocol",
    "IoC": "Indicators of Compromise",
    "IoT": "Internet of Things",
    "IP": "Internet Protocol",
    "IPS": "Intrusion Prevention System",
    "IPSec": "Internet Protocol Security",
    "IR": "Incident Response",
    "IRP": "Incident Response Plan",
    "ISO": "International Organization for Standardization",
    "ISP": "Internet Service Provider",
    "ISSO": "Information Systems Security Officer",
    "IV": "Initialization Vector",
    "KDC": "Key Distribution Center",
    "KEK": "Key Encryption Key",
    "L2TP": "Layer 2 Tunneling Protocol",
    "LAN": "Local Area Network",
    "LDAP": "Lightweight Directory Access Protocol",
    "LDAPS": "Lightweight Directory Access Protocol Secure",
    "MaaS": "Monitoring as a Service",
    "MAC": "Mandatory Access Control / Media Access Control / Message Authentication Code",
    "MBR": "Master Boot Record",
    "MD5": "Message Digest 5",
    "MDM": "Mobile Device Management",
    "MFA": "Multifactor Authentication",
    "MFD": "Multifunction Device",
    "MFP": "Multifunction Printer",
    "ML": "Machine Learning",
    "MMS": "Multimedia Message Service",
    "MOA": "Memorandum of Agreement",
    "MOU": "Memorandum of Understanding",
    "MPLS": "Multiprotocol Label Switching",
    "MSA": "Master Service Agreement",
    "MSCHAP": "Microsoft Challenge Handshake Authentication Protocol",
    "MSP": "Managed Service Provider",
    "MSSP": "Managed Security Service Provider",
    "MTBF": "Mean Time Between Failures",
    "MTTF": "Mean Time to Failure",
    "MTTR": "Mean Time to Repair",
    "MTU": "Maximum Transmission Unit",
    "NAC": "Network Access Control",
    "NAT": "Network Address Translation",
    "NDA": "Non-Disclosure Agreement",
    "NFC": "Near-Field Communication",
    "NGFW": "Next-Generation Firewall",
    "NIDS": "Network-based Intrusion Detection System",
    "NIPS": "Network-based Intrusion Prevention System",
    "NIST": "National Institute of Standards and Technology",
    "NTFS": "New Technology File System",
    "NTLM": "New Technology LAN Manager",
    "NTP": "Network Time Protocol",
    "OAuth": "Open Authorization",
    "OCSP": "Online Certificate Status Protocol",
    "OID": "Object Identifier",
    "OS": "Operating System",
    "OSINT": "Open-Source Intelligence",
    "OSPF": "Open Shortest Path First",
    "OT": "Operational Technology",
    "OTA": "Over the Air",
    "OVAL": "Open Vulnerability Assessment Language",
    "P12": "PKCS #12",
    "P2P": "Peer to Peer",
    "PaaS": "Platform as a Service",
    "PAC": "Proxy Auto Configuration",
    "PAM": "Privileged Access Management / Pluggable Authentication Modules",
    "PAP": "Password Authentication Protocol",
    "PAT": "Port Address Translation",
    "PBKDF2": "Password-Based Key Derivation Function 2",
    "PBX": "Private Branch Exchange",
    "PCAP": "Packet Capture",
    "PCI DSS": "Payment Card Industry Data Security Standard",
    "PDU": "Power Distribution Unit",
    "PEAP": "Protected Extensible Authentication Protocol",
    "PED": "Personal Electronic Device",
    "PEM": "Privacy Enhanced Mail",
    "PFS": "Perfect Forward Secrecy",
    "PGP": "Pretty Good Privacy",
    "PHI": "Protected Health Information",
    "PII": "Personally Identifiable Information",
    "PIV": "Personal Identity Verification",
    "PKCS": "Public Key Cryptography Standards",
    "PKI": "Public Key Infrastructure",
    "POP3": "Post Office Protocol 3",
    "PPP": "Point-to-Point Protocol",
    "PPTP": "Point-to-Point Tunneling Protocol",
    "PSK": "Pre-Shared Key",
    "PTZ": "Pan-Tilt-Zoom",
    "PUP": "Potentially Unwanted Program",
    "RA": "Registration Authority / Recovery Agent",
    "RADIUS": "Remote Authentication Dial-In User Service",
    "RAID": "Redundant Array of Inexpensive Disks",
    "RAS": "Remote Access Server",
    "RAT": "Remote Access Trojan",
    "RBAC": "Role-Based Access Control / Rule-Based Access Control",
    "RC4": "Rivest Cipher 4",
    "RDP": "Remote Desktop Protocol",
    "RFID": "Radio Frequency Identification",
    "RIPEMD": "RACE Integrity Primitives Evaluation Message Digest",
    "ROI": "Return on Investment",
    "RPO": "Recovery Point Objective",
    "RSA": "Rivest, Shamir, and Adleman",
    "RTBH": "Remotely Triggered Black Hole",
    "RTO": "Recovery Time Objective",
    "RTOS": "Real-Time Operating System",
    "RTP": "Real-Time Transport Protocol",
    "S/MIME": "Secure/Multipurpose Internet Mail Extensions",
    "SaaS": "Software as a Service",
    "SAE": "Simultaneous Authentication of Equals",
    "SAML": "Security Assertion Markup Language",
    "SAN": "Storage Area Network / Subject Alternative Name",
    "SASE": "Secure Access Service Edge",
    "SCADA": "Supervisory Control and Data Acquisition",
    "SCAP": "Security Content Automation Protocol",
    "SCEP": "Simple Certificate Enrollment Protocol",
    "SD-WAN": "Software-Defined Wide Area Network",
    "SDK": "Software Development Kit",
    "SDLC": "Software Development Lifecycle",
    "SDN": "Software-Defined Networking",
    "SED": "Self-Encrypting Drive",
    "SFTP": "SSH File Transfer Protocol",
    "SHA": "Secure Hashing Algorithm",
    "SIEM": "Security Information and Event Management",
    "SIM": "Subscriber Identity Module",
    "SLA": "Service-Level Agreement",
    "SLE": "Single Loss Expectancy",
    "SMS": "Short Message Service",
    "SMTP": "Simple Mail Transfer Protocol",
    "SMTPS": "Simple Mail Transfer Protocol Secure",
    "SNMP": "Simple Network Management Protocol",
    "SOAR": "Security Orchestration, Automation, and Response",
    "SOC": "Security Operations Center",
    "SOW": "Statement of Work",
    "SPF": "Sender Policy Framework",
    "SQL": "Structured Query Language",
    "SQLi": "SQL Injection",
    "SRTP": "Secure Real-Time Transport Protocol",
    "SSD": "Solid State Drive",
    "SSH": "Secure Shell",
    "SSL": "Secure Sockets Layer",
    "SSO": "Single Sign-On",
    "STIX": "Structured Threat Information eXchange",
    "SWG": "Secure Web Gateway",
    "TACACS+": "Terminal Access Controller Access Control System Plus",
    "TAXII": "Trusted Automated eXchange of Indicator Information",
    "TGT": "Ticket Granting Ticket",
    "TKIP": "Temporal Key Integrity Protocol",
    "TLS": "Transport Layer Security",
    "TOC": "Time-of-Check",
    "TOTP": "Time-based One-Time Password",
    "TOU": "Time-of-Use",
    "TPM": "Trusted Platform Module",
    "TTP": "Tactics, Techniques, and Procedures",
    "UAT": "User Acceptance Testing",
    "UDP": "User Datagram Protocol",
    "UEFI": "Unified Extensible Firmware Interface",
    "UEM": "Unified Endpoint Management",
    "UPS": "Uninterruptible Power Supply",
    "URI": "Uniform Resource Identifier",
    "URL": "Uniform Resource Locator",
    "USB": "Universal Serial Bus",
    "UTM": "Unified Threat Management",
    "VBA": "Visual Basic for Applications",
    "VDI": "Virtual Desktop Infrastructure",
    "VLAN": "Virtual Local Area Network",
    "VM": "Virtual Machine",
    "VoIP": "Voice over Internet Protocol",
    "VPC": "Virtual Private Cloud",
    "VPN": "Virtual Private Network",
    "WAF": "Web Application Firewall",
    "WAP": "Wireless Access Point",
    "WEP": "Wired Equivalent Privacy",
    "WIDS": "Wireless Intrusion Detection System",
    "WIPS": "Wireless Intrusion Prevention System",
    "WO": "Work Order",
    "WPA": "Wi-Fi Protected Access",
    "WPS": "Wi-Fi Protected Setup",
    "XDR": "Extended Detection and Response",
    "XML": "Extensible Markup Language",
    "XOR": "Exclusive Or",
    "XSRF": "Cross-Site Request Forgery",
    "XSS": "Cross-Site Scripting",
}


def acronym_blitz(rounds=20):
    banner("ACRONYM BLITZ", C.MAGENTA)
    print(wrap(f"This blitz drills {len(ACRONYMS)} entries from the official "
               "SY0-701 acronym list — CompTIA expects you to know them all. "
               "Type the expansion; "
               "close answers are auto-judged, borderline ones you self-grade. "
               "For multi-meaning acronyms any one expansion counts. q to stop."))
    items = random.sample(list(ACRONYMS.items()), min(rounds, len(ACRONYMS)))
    score, asked = 0, 0
    try:
        for n, (abbr, full) in enumerate(items, 1):
            print()
            print(wrap(f"{n}. {C.BOLD}{abbr}{C.RESET} stands for...?"))
            ans = normalize(get_input("  Expansion: "))
            targets = [normalize(t) for t in full.split(" / ")]
            ratio = max(difflib.SequenceMatcher(None, ans, t).ratio()
                        for t in targets)
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
