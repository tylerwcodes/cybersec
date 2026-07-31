"""Special drills: Azure gym (generated problems), service blitz, acronym blitz.

The service table and acronym list are built from the official AZ-900
"Skills measured" outline (Describe cloud concepts / Azure architecture and
services / Azure management and governance).
"""
import difflib
import random

from engine import (C, QuitRound, banner, get_input, grade_line, normalize,
                    wrap)

# ---------------------------------------------------------------- services ---
# (name, category, one-line description, accepted answers for reverse mode)
SERVICES = [
    ("Azure Virtual Machines", "compute",
     "IaaS - rent Windows/Linux servers with full OS control; you patch and manage them",
     ["azure virtual machines", "virtual machines", "virtual machine", "vm", "vms", "azure vm"]),
    ("Virtual Machine Scale Sets", "compute",
     "Deploy and auto-scale a group of identical, load-balanced VMs",
     ["virtual machine scale sets", "vm scale sets", "vmss", "scale sets", "scale set"]),
    ("Availability Sets", "compute",
     "Spread VMs across fault domains and update domains within a datacenter to survive hardware failures and maintenance",
     ["availability sets", "availability set"]),
    ("Azure App Service", "compute",
     "PaaS - host web apps and REST APIs without managing the OS or web server",
     ["azure app service", "app service", "web apps", "app services"]),
    ("Azure Functions", "compute",
     "Serverless - run small pieces of event-driven code; billed only while the code runs",
     ["azure functions", "functions", "function apps", "azure function"]),
    ("Azure Container Instances", "compute",
     "Run a single container on demand without managing servers or an orchestrator",
     ["azure container instances", "container instances", "aci"]),
    ("Azure Kubernetes Service", "compute",
     "Managed Kubernetes cluster for orchestrating many containers",
     ["azure kubernetes service", "kubernetes service", "aks"]),
    ("Azure Container Apps", "compute",
     "Serverless container hosting with scaling and load balancing built in - no orchestrator to manage",
     ["azure container apps", "container apps"]),
    ("Azure Virtual Desktop", "compute",
     "Windows desktops and apps streamed from the cloud to any device, supporting multi-session Windows",
     ["azure virtual desktop", "virtual desktop", "avd"]),
    ("Azure Virtual Network", "networking",
     "Your isolated private network in Azure - defines address space and subnets for your resources",
     ["azure virtual network", "virtual network", "vnet", "virtual networks", "vnets"]),
    ("Virtual network peering", "networking",
     "Connects two virtual networks over the Microsoft backbone so they act as one network",
     ["virtual network peering", "vnet peering", "peering"]),
    ("Network Security Group", "networking",
     "Filters inbound/outbound traffic to subnets and NICs with allow/deny security rules",
     ["network security group", "network security groups", "nsg", "nsgs"]),
    ("Azure VPN Gateway", "networking",
     "Encrypted IPsec tunnel over the public Internet connecting on-premises networks (or clients) to a VNet",
     ["azure vpn gateway", "vpn gateway", "vpn"]),
    ("Azure ExpressRoute", "networking",
     "Dedicated private circuit into Microsoft's network that bypasses the public Internet entirely",
     ["azure expressroute", "expressroute", "express route"]),
    ("Azure DNS", "networking",
     "Hosts DNS domains/zones and answers name-resolution queries using Azure's global infrastructure",
     ["azure dns", "dns"]),
    ("Private endpoint", "networking",
     "Gives a PaaS service a private IP inside your VNet so it is reachable without public exposure",
     ["private endpoint", "private endpoints", "private link"]),
    ("Azure Load Balancer", "networking",
     "Distributes incoming network traffic across a group of backend VMs",
     ["azure load balancer", "load balancer"]),
    ("Azure Blob Storage", "storage",
     "Object storage for unstructured data (documents, images, backups, logs) with Hot/Cool/Cold/Archive tiers",
     ["azure blob storage", "blob storage", "blobs", "blob"]),
    ("Azure Files", "storage",
     "Fully managed cloud file shares mounted over SMB or NFS, usable from cloud or on-premises",
     ["azure files", "files", "azure file shares", "file shares"]),
    ("Azure Queue Storage", "storage",
     "Stores large numbers of small messages so application components can communicate asynchronously",
     ["azure queue storage", "queue storage", "queues", "queue"]),
    ("Azure Table Storage", "storage",
     "NoSQL key/attribute store for large amounts of structured, non-relational data",
     ["azure table storage", "table storage", "tables"]),
    ("Azure Managed Disks", "storage",
     "Block-level storage volumes (like virtual hard disks) attached to Azure VMs",
     ["azure managed disks", "managed disks", "disk storage", "disks"]),
    ("Azure File Sync", "storage",
     "Caches Azure file shares on an on-premises Windows Server while keeping them centralized in Azure",
     ["azure file sync", "file sync"]),
    ("AzCopy", "storage",
     "Command-line utility for copying blobs and files to/from storage accounts, including sync",
     ["azcopy", "az copy"]),
    ("Azure Storage Explorer", "storage",
     "Standalone GUI app for browsing and moving data in storage accounts across platforms",
     ["azure storage explorer", "storage explorer"]),
    ("Azure Migrate", "migration",
     "Hub that discovers, assesses, and migrates on-premises servers, databases, and apps to Azure",
     ["azure migrate", "migrate"]),
    ("Azure Data Box", "migration",
     "Physical ruggedized appliance shipped to you for offline transfer of large datasets (up to ~80 TB) into or out of Azure",
     ["azure data box", "data box", "databox"]),
    ("Microsoft Entra ID", "identity",
     "Cloud-based identity and access management service - users, sign-in, SSO, MFA (formerly Azure Active Directory)",
     ["microsoft entra id", "entra id", "entra", "azure active directory", "azure ad", "aad"]),
    ("Microsoft Entra Domain Services", "identity",
     "Managed domain services (domain join, group policy, LDAP, Kerberos/NTLM) without running your own domain controllers",
     ["microsoft entra domain services", "entra domain services", "domain services", "azure ad ds"]),
    ("Conditional Access", "identity",
     "If-then policies that allow, block, or require MFA for sign-ins based on user, location, device, and risk signals",
     ["conditional access", "microsoft entra conditional access"]),
    ("Azure role-based access control", "identity",
     "Grants permissions by assigning roles (e.g., Owner, Contributor, Reader) to identities at a chosen scope",
     ["azure role based access control", "role based access control", "rbac", "azure rbac"]),
    ("Microsoft Defender for Cloud", "security",
     "Cloud security posture management and workload protection - secure score, recommendations, threat alerts",
     ["microsoft defender for cloud", "defender for cloud", "defender"]),
    ("Azure Policy", "governance",
     "Creates, assigns, and evaluates rules that enforce standards (e.g., allowed regions/SKUs) across resources, with compliance reporting",
     ["azure policy", "policy"]),
    ("Resource locks", "governance",
     "Prevent accidental deletion (CanNotDelete) or modification (ReadOnly) of resources regardless of RBAC",
     ["resource locks", "resource lock", "locks", "lock"]),
    ("Tags", "governance",
     "Name/value metadata pairs on resources for organizing and reporting - commonly cost center, environment, owner",
     ["tags", "tag", "resource tags"]),
    ("Microsoft Purview", "governance",
     "Unified data governance - maps, catalogs, and classifies data across Azure, on-premises, and other clouds",
     ["microsoft purview", "purview"]),
    ("Azure Arc", "management",
     "Extends Azure management (Policy, RBAC, tags) to servers and Kubernetes running on-premises or in other clouds",
     ["azure arc", "arc"]),
    ("Azure Resource Manager", "management",
     "The deployment and management layer for Azure - every portal/CLI/PowerShell request goes through it",
     ["azure resource manager", "resource manager", "arm"]),
    ("ARM templates", "management",
     "Declarative JSON files that deploy Azure infrastructure repeatably (infrastructure as code)",
     ["arm templates", "arm template", "azure resource manager templates", "templates"]),
    ("Bicep", "management",
     "Simpler declarative language that transpiles to ARM templates for infrastructure as code",
     ["bicep"]),
    ("Azure Cloud Shell", "management",
     "Browser-based shell in the portal with Azure CLI and Azure PowerShell preinstalled - nothing to install locally",
     ["azure cloud shell", "cloud shell"]),
    ("Azure CLI", "management",
     "Cross-platform command-line tool using 'az' commands to manage Azure resources",
     ["azure cli", "cli", "az cli"]),
    ("Azure PowerShell", "management",
     "PowerShell cmdlets (Az module) for managing Azure resources from scripts and automation",
     ["azure powershell", "powershell"]),
    ("Azure Advisor", "monitoring",
     "Free personalized recommendations across reliability, security, performance, operational excellence, and cost",
     ["azure advisor", "advisor"]),
    ("Azure Service Health", "monitoring",
     "Tells you about Azure platform incidents, planned maintenance, and health advisories affecting YOUR resources",
     ["azure service health", "service health"]),
    ("Azure Monitor", "monitoring",
     "Platform for collecting, analyzing, and acting on metrics and logs from Azure and on-premises resources",
     ["azure monitor", "monitor"]),
    ("Log Analytics", "monitoring",
     "Workspace and query tool (KQL) for analyzing log data collected by Azure Monitor",
     ["log analytics", "log analytics workspace"]),
    ("Application Insights", "monitoring",
     "Azure Monitor feature that instruments applications to track performance, requests, failures, and usage",
     ["application insights", "app insights"]),
    ("Pricing calculator", "cost",
     "Estimates the cost of Azure services you plan to deploy - configure services and get a monthly estimate",
     ["pricing calculator", "azure pricing calculator"]),
    ("TCO Calculator", "cost",
     "Compares the cost of running workloads on-premises vs. in Azure over multiple years",
     ["tco calculator", "total cost of ownership calculator", "tco"]),
    ("Microsoft Cost Management", "cost",
     "Analyzes actual Azure spending, sets budgets, and sends alerts when spending approaches limits",
     ["microsoft cost management", "cost management", "cost management and billing"]),
]

CATEGORY_ALIASES = {
    "compute": ["compute"],
    "networking": ["networking", "network"],
    "storage": ["storage"],
    "migration": ["migration", "migrate"],
    "identity": ["identity", "identity and access", "iam"],
    "security": ["security"],
    "governance": ["governance", "governance and compliance", "compliance"],
    "management": ["management", "management and deployment", "deployment"],
    "monitoring": ["monitoring", "monitor"],
    "cost": ["cost", "cost management"],
}


def service_blitz(rounds=15):
    banner("SERVICE BLITZ", C.MAGENTA)
    print(wrap(f"{len(SERVICES)} core AZ-900 services. Forward: name the service "
               "from its description. Reverse: give the service's category "
               "(compute / networking / storage / migration / identity / security / "
               "governance / management / monitoring / cost). Type q to stop."))
    score, streak, best_streak = 0, 0, 0
    asked = 0
    try:
        for n in range(1, rounds + 1):
            name, cat, desc, accepted = random.choice(SERVICES)
            forward = random.random() < 0.65
            print()
            if forward:
                print(wrap(f"{n}. Which Azure service/tool is this: "
                           f"{C.BOLD}{desc}{C.RESET}?"))
                ans = normalize(get_input("  Service: "))
                targets = [normalize(a) for a in accepted]
                ok = ans in targets or any(
                    difflib.SequenceMatcher(None, ans, t).ratio() >= 0.85
                    for t in targets if ans)
            else:
                print(wrap(f"{n}. What category does {C.BOLD}{name}{C.RESET} belong to?"))
                ans = normalize(get_input("  Category: "))
                ok = ans in [normalize(a) for a in CATEGORY_ALIASES[cat]]
            asked += 1
            if ok:
                score += 1
                streak += 1
                best_streak = max(best_streak, streak)
                flame = " 🔥" * min(3, streak // 3)
                print(C.GREEN + C.BOLD + f"  ✔ Correct! (streak {streak}){flame}" + C.RESET)
            else:
                streak = 0
                print(C.RED + C.BOLD + f"  ✘ {name} ({cat})" + C.RESET)
            print(C.DIM + wrap(f"    {name}: {desc}", indent=4) + C.RESET)
    except QuitRound:
        pass
    if asked:
        print()
        print(grade_line(score, asked))
        print(C.DIM + f"  Best streak: {best_streak}" + C.RESET)


# ---------------------------------------------------------------- acronyms ---
# Acronyms and short names an AZ-900 candidate should be able to expand.
ACRONYMS = {
    "ACI": "Azure Container Instances",
    "AKS": "Azure Kubernetes Service",
    "API": "Application Programming Interface",
    "ARM": "Azure Resource Manager",
    "AVD": "Azure Virtual Desktop",
    "B2B": "Business to Business",
    "B2C": "Business to Consumer",
    "CapEx": "Capital Expenditure",
    "CDN": "Content Delivery Network",
    "CLI": "Command-Line Interface",
    "CSPM": "Cloud Security Posture Management",
    "DDoS": "Distributed Denial of Service",
    "DNS": "Domain Name System",
    "FIDO2": "Fast Identity Online 2",
    "GRS": "Geo-Redundant Storage",
    "GZRS": "Geo-Zone-Redundant Storage",
    "HTTPS": "Hypertext Transfer Protocol Secure",
    "IaaS": "Infrastructure as a Service",
    "IaC": "Infrastructure as Code",
    "IoT": "Internet of Things",
    "JSON": "JavaScript Object Notation",
    "KQL": "Kusto Query Language",
    "LRS": "Locally Redundant Storage",
    "MFA": "Multifactor Authentication",
    "NFS": "Network File System",
    "NIC": "Network Interface Card",
    "NSG": "Network Security Group",
    "OpEx": "Operational Expenditure",
    "OS": "Operating System",
    "P2S": "Point-to-Site",
    "PaaS": "Platform as a Service",
    "RA-GRS": "Read-Access Geo-Redundant Storage",
    "RA-GZRS": "Read-Access Geo-Zone-Redundant Storage",
    "RBAC": "Role-Based Access Control",
    "RDP": "Remote Desktop Protocol",
    "REST": "Representational State Transfer",
    "S2S": "Site-to-Site",
    "SaaS": "Software as a Service",
    "SLA": "Service-Level Agreement",
    "SMB": "Server Message Block",
    "SQL": "Structured Query Language",
    "SSH": "Secure Shell",
    "SSO": "Single Sign-On",
    "TCO": "Total Cost of Ownership",
    "TLS": "Transport Layer Security",
    "VM": "Virtual Machine",
    "VMSS": "Virtual Machine Scale Sets",
    "VNet": "Virtual Network",
    "VPN": "Virtual Private Network",
    "ZRS": "Zone-Redundant Storage",
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
    print(wrap(f"{total} acronyms and short names from the AZ-900 world. "
               "Type the expansion; close answers are auto-judged, borderline "
               "ones you self-grade. q to stop."))
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


# --------------------------------------------------------------- Azure gym ---
# Level 1: shared responsibility. Level 2: scope & hierarchy. Level 3:
# storage redundancy + SLA downtime math. Problems are generated live.

# Microsoft's shared responsibility chart. Values per (on-prem, IaaS, PaaS, SaaS).
RESPONSIBILITY = [
    ("Information and data", ("customer", "customer", "customer", "customer")),
    ("Devices (mobile and PCs)", ("customer", "customer", "customer", "customer")),
    ("Accounts and identities", ("customer", "customer", "customer", "customer")),
    ("Identity and directory infrastructure",
     ("customer", "customer", "shared", "shared")),
    ("Applications", ("customer", "customer", "shared", "microsoft")),
    ("Network controls", ("customer", "customer", "shared", "microsoft")),
    ("Operating system", ("customer", "customer", "microsoft", "microsoft")),
    ("Physical hosts", ("customer", "microsoft", "microsoft", "microsoft")),
    ("Physical network", ("customer", "microsoft", "microsoft", "microsoft")),
    ("Physical datacenter", ("customer", "microsoft", "microsoft", "microsoft")),
]
MODELS = ["on-premises", "IaaS", "PaaS", "SaaS"]

RESP_ACCEPT = {
    "customer": ["customer", "you", "the customer", "customer responsibility", "c"],
    "microsoft": ["microsoft", "azure", "the provider", "provider", "cloud provider", "m"],
    "shared": ["shared", "both", "s"],
}

# (SLA %, downtime per 30-day month in minutes)
SLA_TABLE = [
    ("99", 432.0),
    ("99.9", 43.2),
    ("99.95", 21.6),
    ("99.99", 4.32),
    ("99.999", 0.432),
]

REDUNDANCY = [
    ("LRS", "Locally Redundant Storage", 3,
     "3 synchronous copies in ONE datacenter - cheapest, no zone or region protection"),
    ("ZRS", "Zone-Redundant Storage", 3,
     "3 synchronous copies across THREE availability zones in the primary region"),
    ("GRS", "Geo-Redundant Storage", 6,
     "LRS in the primary region + 3 async copies (LRS) in the secondary region"),
    ("GZRS", "Geo-Zone-Redundant Storage", 6,
     "ZRS in the primary region + 3 async copies (LRS) in the secondary region"),
]

HIERARCHY = ["management group", "subscription", "resource group", "resource"]

# (question, answer_key, explanation) - answer_key in yes/no
SCOPE_FACTS = [
    ("Can a single resource belong to two resource groups at the same time?",
     "no", "A resource lives in exactly one resource group (though it can be moved)."),
    ("Can a resource group contain resources from different Azure regions?",
     "yes", "A resource group has its own location (for metadata), but the resources inside it can be in any region."),
    ("If you delete a resource group, are all resources inside it deleted too?",
     "yes", "Deleting a resource group deletes everything in it - which is why ReadOnly/CanNotDelete locks matter."),
    ("Can a subscription belong to more than one management group?",
     "no", "Each subscription (and each management group) has exactly one parent management group."),
    ("Can management groups be nested inside other management groups?",
     "yes", "Management groups support up to six levels of depth (not counting root and subscription level)."),
    ("Does a policy assigned to a management group apply to every subscription under it?",
     "yes", "Settings applied at a scope are inherited by all child scopes - that's the point of management groups."),
    ("Can a virtual machine's disk resources live in a different resource group than the VM?",
     "yes", "Related resources can be split across groups, though keeping a workload's resources together (shared lifecycle) is the best practice."),
    ("Does a ReadOnly resource lock override permissions granted through RBAC?",
     "yes", "Locks apply regardless of RBAC - even an Owner must remove the lock before deleting or modifying."),
    ("Can one organization have multiple Azure subscriptions?",
     "yes", "Organizations commonly use separate subscriptions per environment, department, or billing boundary."),
]


def _gym_question(level):
    """Returns go() -> (bool, explanation_str)."""
    if level == 1:
        area, answers = random.choice(RESPONSIBILITY)
        mi = random.randint(0, 3)
        model = MODELS[mi]
        answer = answers[mi]

        def go():
            print(wrap(f"In an {model} deployment, who is responsible for: "
                       f"{C.BOLD}{area}{C.RESET}?  (customer / Microsoft / shared)"))
            ans = normalize(get_input("  Who: "))
            ok = ans in [normalize(a) for a in RESP_ACCEPT[answer]]
            row = ", ".join(f"{m}: {a}" for m, a in zip(MODELS, answers))
            return ok, (f"{area} under {model} = {answer.upper()}. "
                        f"Full row - {row}. You ALWAYS retain data, devices, "
                        "and identities; Microsoft always owns the physical layer in the cloud.")
        return go

    if level == 2:
        kind = random.choice(["order", "fact", "parent", "child"])
        if kind == "order":
            shuffled = HIERARCHY[:]
            while shuffled == HIERARCHY:
                random.shuffle(shuffled)

            def go():
                print(wrap("Order these scopes from TOP (broadest) to BOTTOM "
                           "(most specific):"))
                for i, item in enumerate(shuffled, 1):
                    print(f"    {i}. {item}")
                raw = get_input("  Order (e.g. '3 1 4 2'): ").replace(",", " ").split()
                try:
                    seq = [shuffled[int(x) - 1] for x in raw]
                except (ValueError, IndexError):
                    seq = None
                ok = seq == HIERARCHY
                return ok, ("Top to bottom: management group > subscription > "
                            "resource group > resource. Policy, RBAC, and locks "
                            "applied high flow down to everything beneath.")
            return go

        if kind in ("parent", "child"):
            i = random.randint(1, len(HIERARCHY) - 1)

            def go():
                if kind == "parent":
                    print(wrap(f"In the Azure hierarchy, what scope sits DIRECTLY "
                               f"ABOVE a {C.BOLD}{HIERARCHY[i]}{C.RESET}?"))
                    expected = HIERARCHY[i - 1]
                else:
                    print(wrap(f"In the Azure hierarchy, what scope sits DIRECTLY "
                               f"BELOW a {C.BOLD}{HIERARCHY[i - 1]}{C.RESET}?"))
                    expected = HIERARCHY[i]
                ans = normalize(get_input("  Scope: "))
                accepted = [expected, expected + "s"]
                ok = ans in [normalize(a) for a in accepted]
                return ok, ("Hierarchy: management group > subscription > "
                            f"resource group > resource. Answer: {expected}.")
            return go

        q, key, why = random.choice(SCOPE_FACTS)

        def go():
            print(wrap(q + "  (y/n)"))
            ans = get_input("  y/n: ").lower()
            ok = ans.startswith("y") == (key == "yes")
            return ok, f"Answer: {key.upper()}. {why}"
        return go

    # level 3 - redundancy + SLA
    kind = random.choice(["copies", "pick_redundancy", "downtime", "compare_sla"])
    if kind == "copies":
        abbr, full, copies, why = random.choice(REDUNDANCY)

        def go():
            print(wrap(f"How many total copies of your data does "
                       f"{C.BOLD}{full} ({abbr}){C.RESET} keep?"))
            ans = get_input("  Copies: ").strip()
            ok = ans == str(copies)
            return ok, f"{abbr} = {copies} copies. {why}"
        return go

    if kind == "pick_redundancy":
        scenarios = [
            ("the cheapest redundancy, no protection needed beyond one datacenter", "LRS"),
            ("survive a whole datacenter (zone) failure, but data must stay in one region", "ZRS"),
            ("survive the loss of an entire region (secondary region copy), lowest cost that does so", "GRS"),
            ("survive both a zone failure AND a regional disaster", "GZRS"),
        ]
        want, expected = random.choice(scenarios)

        def go():
            print(wrap(f"Which storage redundancy option fits: {C.BOLD}{want}{C.RESET}? "
                       "(LRS / ZRS / GRS / GZRS)"))
            ans = normalize(get_input("  Option: ")).replace(" ", "")
            ok = ans == expected.lower()
            why = next(r[3] for r in REDUNDANCY if r[0] == expected)
            return ok, f"{expected}: {why}"
        return go

    if kind == "downtime":
        sla, minutes = random.choice(SLA_TABLE)

        def go():
            print(wrap(f"A service has a {C.BOLD}{sla}%{C.RESET} SLA. What is the "
                       "maximum downtime per 30-day month, in MINUTES? "
                       "(within 5% counts)"))
            ans = get_input("  Minutes: ").replace(",", "").strip()
            try:
                val = float(ans)
                ok = abs(val - minutes) <= max(0.05 * minutes, 0.05)
            except ValueError:
                ok = False
            pct = round(100 - float(sla), 3)
            return ok, (f"{sla}% up = {pct}% down. 30 days = 43,200 minutes; "
                        f"{pct}% of 43,200 = {minutes:g} minutes/month.")
        return go

    # compare_sla
    (sla_a, min_a), (sla_b, min_b) = random.sample(SLA_TABLE, 2)

    def go():
        print(wrap(f"Which SLA allows MORE downtime: {C.BOLD}{sla_a}%{C.RESET} "
                   f"or {C.BOLD}{sla_b}%{C.RESET}?"))
        ans = normalize(get_input("  SLA: ")).rstrip("%")
        expected = sla_a if min_a > min_b else sla_b
        ok = ans == expected
        return ok, (f"{sla_a}% allows {min_a:g} min/month; {sla_b}% allows "
                    f"{min_b:g} min/month. Lower SLA percentage = more allowed "
                    "downtime. Each extra 9 cuts downtime ~10x.")
    return go


def azure_gym():
    banner("AZURE GYM", C.MAGENTA)
    print("""
  1) Level 1 - Shared responsibility  (who manages what: on-prem/IaaS/PaaS/SaaS)
  2) Level 2 - Scope & hierarchy      (management groups, subscriptions, RGs, inheritance)
  3) Level 3 - Redundancy & SLAs      (LRS/ZRS/GRS/GZRS copies, downtime math)
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
            go = _gym_question(level)
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
