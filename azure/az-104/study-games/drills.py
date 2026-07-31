"""Special drills: Azure gym (generated problems), service blitz, acronym blitz.

The service table and acronym list are built from the official AZ-104
"Skills measured" outline (identities and governance / storage / compute /
virtual networking / monitoring and backup). Gym problems are generated
live with real subnet, RBAC, NSG, and availability math.
"""
import difflib
import math
import random

from engine import (C, QuitRound, banner, get_input, grade_line, normalize,
                    wrap)

# ---------------------------------------------------------------- services ---
# (name, category, one-line description, accepted answers for reverse mode)
SERVICES = [
    # ---- identity ----
    ("Microsoft Entra ID", "identity",
     "Cloud identity and access management - create users and groups, assign licenses, register devices, control sign-in",
     ["microsoft entra id", "entra id", "entra", "azure active directory", "azure ad", "aad"]),
    ("Dynamic groups", "identity",
     "Entra groups whose membership is auto-populated by rules on user or device attributes (e.g. department equals Sales)",
     ["dynamic groups", "dynamic group", "dynamic membership groups", "dynamic membership"]),
    ("Self-service password reset", "identity",
     "Lets users reset their own Entra passwords after verifying with registered methods - you choose which groups are enabled",
     ["self service password reset", "sspr", "password reset"]),
    ("Administrative units", "identity",
     "Restrict an Entra role's reach to a subset of users, groups, or devices - e.g. one region's helpdesk manages only that region",
     ["administrative units", "administrative unit", "admin units", "admin unit"]),
    ("Managed identity", "identity",
     "An automatically managed Entra identity for an Azure resource so it can authenticate to other services with no stored credentials",
     ["managed identity", "managed identities", "msi", "system assigned managed identity"]),
    # ---- governance ----
    ("Azure Policy", "governance",
     "Define and evaluate rules resources must follow (allowed regions, required tags, SKUs) with audit, deny, and deployIfNotExists effects",
     ["azure policy", "policy"]),
    ("Policy initiative", "governance",
     "A group of policy definitions assigned together and tracked as a single compliance score",
     ["policy initiative", "initiative", "initiatives", "policy set", "initiative definition"]),
    ("Resource locks", "governance",
     "CanNotDelete or ReadOnly protection on a resource, resource group, or subscription that applies regardless of RBAC",
     ["resource locks", "resource lock", "locks", "lock"]),
    ("Tags", "governance",
     "Name/value metadata on resources and groups for cost reporting and organization - not inherited by child resources by default",
     ["tags", "tag", "resource tags"]),
    ("Management groups", "governance",
     "Containers above subscriptions for organizing them and applying policy and RBAC at scale - nest up to six levels deep",
     ["management groups", "management group", "mg", "mgs"]),
    ("Microsoft Cost Management", "governance",
     "Analyze actual spend, create budgets, and fire alerts as spending approaches the limits you set",
     ["microsoft cost management", "cost management", "cost management and billing"]),
    ("Azure Advisor", "governance",
     "Free personalized recommendations across cost, security, reliability, performance, and operational excellence",
     ["azure advisor", "advisor"]),
    # ---- storage ----
    ("Storage account", "storage",
     "The top-level namespace holding blobs, files, queues, and tables - globally unique name; redundancy and performance tier set here",
     ["storage account", "storage accounts", "azure storage account"]),
    ("Azure Blob Storage", "storage",
     "Object storage for unstructured data with hot, cool, cold, and archive access tiers plus versioning and soft delete",
     ["azure blob storage", "blob storage", "blobs", "blob"]),
    ("Azure Files", "storage",
     "Managed SMB and NFS file shares you can mount from Windows, Linux, macOS, or on-premises servers",
     ["azure files", "files", "azure file shares", "file shares", "file share"]),
    ("Azure File Sync", "storage",
     "Turns a Windows Server into a fast cache of an Azure file share, with cloud tiering of rarely used files",
     ["azure file sync", "file sync"]),
    ("AzCopy", "storage",
     "Command-line tool to copy or sync blobs and files into and out of storage accounts",
     ["azcopy", "az copy"]),
    ("Shared access signature", "storage",
     "A signed URI granting limited, time-boxed permissions to storage resources without handing out account keys",
     ["shared access signature", "sas", "sas token", "shared access signatures"]),
    ("Lifecycle management", "storage",
     "Rule-based automation that moves blobs to cooler tiers or deletes them N days after last modification or access",
     ["lifecycle management", "blob lifecycle management", "lifecycle policy", "lifecycle"]),
    ("Object replication", "storage",
     "Asynchronously copies block blobs between two storage accounts based on container-level rules",
     ["object replication", "blob object replication"]),
    ("Azure Data Box", "storage",
     "Ruggedized appliance shipped to your datacenter for offline bulk transfer of large datasets into Azure",
     ["azure data box", "data box", "databox"]),
    # ---- compute ----
    ("Azure Virtual Machines", "compute",
     "IaaS servers you size, image, patch, and manage - attach disks and NICs, choose a region and redundancy option",
     ["azure virtual machines", "virtual machines", "virtual machine", "vm", "vms", "azure vm"]),
    ("Virtual Machine Scale Sets", "compute",
     "Deploy and autoscale a set of identical VMs behind a load balancer, scaling on metrics or a schedule",
     ["virtual machine scale sets", "vm scale sets", "vmss", "scale sets", "scale set"]),
    ("Availability set", "compute",
     "Spreads VMs across fault domains and update domains within one datacenter - 99.95% SLA with two or more VMs",
     ["availability set", "availability sets"]),
    ("Availability zones", "compute",
     "Physically separate datacenters within a region - VMs spread across zones earn a 99.99% SLA",
     ["availability zones", "availability zone", "zones"]),
    ("Azure Container Registry", "compute",
     "Private registry for storing and managing container images close to your deployments",
     ["azure container registry", "container registry", "acr"]),
    ("Azure Container Instances", "compute",
     "Run a container or container group on demand with per-second billing - no VM or orchestrator to manage",
     ["azure container instances", "container instances", "aci"]),
    ("Azure Kubernetes Service", "compute",
     "Managed Kubernetes - Azure runs the control plane; you manage and pay for the worker node pools",
     ["azure kubernetes service", "kubernetes service", "aks"]),
    ("Azure App Service", "compute",
     "PaaS hosting for web apps and APIs with built-in scaling, custom domains, and TLS certificates",
     ["azure app service", "app service", "web apps", "web app"]),
    ("App Service plan", "compute",
     "The compute an App Service app runs on - SKU and instance count live here, and scaling happens at this level",
     ["app service plan", "app service plans", "service plan"]),
    ("Deployment slots", "compute",
     "Parallel App Service environments (e.g. staging) you can warm up and swap into production with no downtime",
     ["deployment slots", "deployment slot", "slots", "slot", "staging slots"]),
    ("ARM templates", "compute",
     "Declarative JSON files that deploy resources repeatably - supports what-if preview and incremental or complete mode",
     ["arm templates", "arm template", "azure resource manager templates", "templates"]),
    ("Bicep", "compute",
     "Cleaner infrastructure-as-code language that compiles to ARM template JSON - same engine, better authoring",
     ["bicep"]),
    # ---- networking ----
    ("Azure Virtual Network", "networking",
     "Your private address space in Azure, divided into subnets, where NICs get their IP addresses",
     ["azure virtual network", "virtual network", "vnet", "virtual networks", "vnets"]),
    ("Virtual network peering", "networking",
     "Private connection between two VNets over the Microsoft backbone - non-transitive, works across regions (global peering)",
     ["virtual network peering", "vnet peering", "peering", "global peering"]),
    ("Network Security Group", "networking",
     "Priority-ordered allow/deny rules filtering traffic at subnets and NICs - first match wins",
     ["network security group", "network security groups", "nsg", "nsgs"]),
    ("Application security group", "networking",
     "A named group of NICs used as source or destination in NSG rules so rules follow workloads instead of IP addresses",
     ["application security group", "application security groups", "asg", "asgs"]),
    ("Azure Bastion", "networking",
     "Browser-based RDP/SSH to VMs through the portal - no public IPs on the VMs and no exposed 3389/22",
     ["azure bastion", "bastion"]),
    ("Service endpoint", "networking",
     "Extends a subnet's identity to a PaaS service over the backbone so the service firewall can allow just that subnet - the service keeps its public address",
     ["service endpoint", "service endpoints", "vnet service endpoint", "virtual network service endpoint"]),
    ("Private endpoint", "networking",
     "Gives a PaaS service a private IP (a NIC) inside your VNet via Private Link - reachable from peered VNets and on-premises",
     ["private endpoint", "private endpoints", "private link"]),
    ("Route table", "networking",
     "User-defined routes attached to subnets that override Azure's system routes - e.g. send 0.0.0.0/0 through a firewall NVA",
     ["route table", "route tables", "udr", "user defined routes", "user defined route"]),
    ("Azure Load Balancer", "networking",
     "Layer-4 TCP/UDP distribution across backend VMs with health probes - public or internal frontends",
     ["azure load balancer", "load balancer"]),
    ("Application Gateway", "networking",
     "Layer-7 HTTP(S) load balancer with URL-path routing, cookie affinity, TLS termination, and an optional WAF",
     ["application gateway", "app gateway", "azure application gateway"]),
    ("Traffic Manager", "networking",
     "DNS-based global routing to endpoints by priority, weight, performance, or geography - no data flows through it",
     ["traffic manager", "azure traffic manager"]),
    ("Private DNS zone", "networking",
     "Name resolution for a custom domain inside linked VNets, with optional auto-registration of VM records",
     ["private dns zone", "private dns zones", "private dns", "azure private dns"]),
    ("VPN Gateway", "networking",
     "IPsec tunnels over the Internet - site-to-site to on-premises networks or point-to-site for individual clients",
     ["vpn gateway", "azure vpn gateway", "vpn"]),
    ("ExpressRoute", "networking",
     "Private dedicated circuit into Microsoft's network through a connectivity provider - traffic never crosses the public Internet",
     ["expressroute", "azure expressroute", "express route"]),
    ("Network Watcher", "networking",
     "Regional toolbox for network diagnostics - IP flow verify, next hop, packet capture, NSG flow logs, topology",
     ["network watcher", "azure network watcher"]),
    # ---- monitoring & backup ----
    ("Azure Monitor", "monitoring",
     "The platform pipeline for metrics and logs across all resources, with alerts, dashboards, and workbooks",
     ["azure monitor", "monitor"]),
    ("Log Analytics workspace", "monitoring",
     "The store where Azure Monitor log data lands - query it with KQL to analyze and correlate events",
     ["log analytics workspace", "log analytics", "log analytics workspaces"]),
    ("Data collection rule", "monitoring",
     "Tells the Azure Monitor Agent what data to collect from which machines and which workspace to send it to",
     ["data collection rule", "data collection rules", "dcr", "dcrs"]),
    ("Action group", "monitoring",
     "Reusable set of notifications and automation (email, SMS, webhook, runbook) that alert rules trigger",
     ["action group", "action groups"]),
    ("Recovery Services vault", "monitoring",
     "Holds VM, file, and SQL backup data plus Site Recovery configuration - scoped to one region",
     ["recovery services vault", "recovery services vaults", "rsv"]),
    ("Azure Backup", "monitoring",
     "Policy-driven backup for VMs, shares, and databases with soft delete and long-term retention",
     ["azure backup", "backup"]),
    ("Azure Site Recovery", "monitoring",
     "Replicates VMs to another region and orchestrates failover and failback for disaster recovery",
     ["azure site recovery", "site recovery", "asr"]),
]

CATEGORY_ALIASES = {
    "identity": ["identity", "identity and access", "iam", "entra", "identities"],
    "governance": ["governance", "governance and compliance", "compliance",
                   "management", "management and governance"],
    "storage": ["storage"],
    "compute": ["compute"],
    "networking": ["networking", "network", "virtual networking"],
    "monitoring": ["monitoring", "monitor", "monitoring and backup", "backup",
                   "monitoring backup", "monitoring and maintenance"],
}


def service_blitz(rounds=15):
    banner("SERVICE BLITZ", C.MAGENTA)
    print(wrap(f"{len(SERVICES)} core AZ-104 services and features. Forward: name "
               "the service from its description. Reverse: give the service's "
               "category (identity / governance / storage / compute / networking / "
               "monitoring). Type q to stop."))
    score, streak, best_streak = 0, 0, 0
    asked = 0
    try:
        for n in range(1, rounds + 1):
            name, cat, desc, accepted = random.choice(SERVICES)
            forward = random.random() < 0.65
            print()
            if forward:
                print(wrap(f"{n}. Which Azure service/feature is this: "
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
# Acronyms and short names an AZ-104 candidate should be able to expand.
ACRONYMS = {
    "ACA": "Azure Container Apps",
    "ACI": "Azure Container Instances",
    "ACR": "Azure Container Registry",
    "ADE": "Azure Disk Encryption",
    "AKS": "Azure Kubernetes Service",
    "AMA": "Azure Monitor Agent",
    "ARM": "Azure Resource Manager",
    "ASG": "Application Security Group",
    "ASR": "Azure Site Recovery",
    "BGP": "Border Gateway Protocol",
    "CMK": "Customer-Managed Key",
    "CNAME": "Canonical Name",
    "CRR": "Cross-Region Restore",
    "DCR": "Data Collection Rule",
    "DNAT": "Destination Network Address Translation",
    "ER": "ExpressRoute",
    "FQDN": "Fully Qualified Domain Name",
    "GFS": "Grandfather-Father-Son",
    "GRS": "Geo-Redundant Storage",
    "GZRS": "Geo-Zone-Redundant Storage",
    "IaaS": "Infrastructure as a Service",
    "IaC": "Infrastructure as Code",
    "ILB": "Internal Load Balancer",
    "IOPS": "Input/Output Operations Per Second",
    "JIT": "Just-In-Time",
    "KQL": "Kusto Query Language",
    "LRS": "Locally Redundant Storage",
    "MABS": "Microsoft Azure Backup Server",
    "MARS": "Microsoft Azure Recovery Services",
    "NAT": "Network Address Translation",
    "NFS": "Network File System",
    "NSG": "Network Security Group",
    "NVA": "Network Virtual Appliance",
    "P2S": "Point-to-Site",
    "PaaS": "Platform as a Service",
    "PIM": "Privileged Identity Management",
    "PIP": "Public IP Address",
    "PTR": "Pointer Record",
    "RA-GRS": "Read-Access Geo-Redundant Storage",
    "RBAC": "Role-Based Access Control",
    "RPO": "Recovery Point Objective",
    "RTO": "Recovery Time Objective",
    "S2S": "Site-to-Site",
    "SAS": "Shared Access Signature",
    "SLA": "Service-Level Agreement",
    "SMB": "Server Message Block",
    "SNAT": "Source Network Address Translation",
    "SNI": "Server Name Indication",
    "SOA": "Start of Authority",
    "SSE": "Server-Side Encryption",
    "SSPR": "Self-Service Password Reset",
    "TLS": "Transport Layer Security",
    "TTL": "Time to Live",
    "UDR": "User-Defined Route",
    "VHD": "Virtual Hard Disk",
    "VM": "Virtual Machine",
    "VMSS": "Virtual Machine Scale Sets",
    "VNet": "Virtual Network",
    "WAF": "Web Application Firewall",
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
    print(wrap(f"{total} acronyms and short names from the AZ-104 world. "
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
# Level 1: subnetting & CIDR. Level 2: RBAC & scope. Level 3: NSG rule
# evaluation. Level 4: HA & redundancy math. Problems are generated live.

# ------------------------------------------------------------ IP math utils --

def _ip_to_int(ip):
    a, b, c, d = (int(x) for x in ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def _int_to_ip(n):
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))


def _rand_net(prefix):
    """A random /prefix network inside 10.0.0.0/8 (host bits zeroed)."""
    size = 1 << (32 - prefix)
    base = (10 << 24) | random.randrange(1 << 24)
    return base & (0xFFFFFFFF ^ (size - 1))


def _parse_int(s):
    s = s.replace(",", "").strip().lstrip("/")
    try:
        return int(s)
    except ValueError:
        return None


def _parse_float(s):
    s = s.replace(",", "").strip().rstrip("%")
    try:
        return float(s)
    except ValueError:
        return None


def _fuzzy_in(ans, accepted, cutoff=0.88):
    targets = [normalize(a) for a in accepted]
    if ans in targets:
        return True
    return any(difflib.SequenceMatcher(None, ans, t).ratio() >= cutoff
               for t in targets if ans)


# --------------------------------------------------- level 1: subnetting ----

RESERVED_ROLES = [
    (0, "the network address",
     ["network", "network address", "the network address", "subnet address", "net"]),
    (1, "the default gateway",
     ["gateway", "default gateway", "the default gateway", "router"]),
    (2, "Azure DNS",
     ["dns", "azure dns", "dns mapping", "azure dns mapping"]),
    (3, "Azure DNS",
     ["dns", "azure dns", "dns mapping", "azure dns mapping"]),
    (255, "the broadcast address",
     ["broadcast", "broadcast address", "the broadcast address", "network broadcast"]),
]


def _l1_question():
    kind = random.choice(["usable", "fit", "inside", "first", "reserved"])

    if kind == "usable":
        p = random.randint(22, 29)
        size = 1 << (32 - p)
        usable = size - 5

        def go():
            print(wrap(f"An Azure subnet is a {C.BOLD}/{p}{C.RESET}. How many "
                       "USABLE IP addresses does it give you?"))
            val = _parse_int(get_input("  Usable IPs: "))
            ok = val == usable
            return ok, (f"/{p} = 2^(32-{p}) = {size:,} addresses. Azure reserves 5 in "
                        "every subnet (.0 network, .1 default gateway, .2-.3 Azure "
                        f"DNS, last = broadcast): {size:,} - 5 = {usable:,} usable.")
        return go

    if kind == "fit":
        p = random.randint(22, 28)
        low = (1 << (31 - p)) - 4          # one more than the next size down holds
        high = (1 << (32 - p)) - 5         # what /p can hold
        hosts = random.randint(low, high)

        def go():
            print(wrap(f"You need a subnet with room for {C.BOLD}{hosts}{C.RESET} "
                       "usable IPs. What is the SMALLEST Azure subnet that fits? "
                       "(answer as /N)"))
            val = _parse_int(get_input("  Prefix: "))
            ok = val == p
            return ok, (f"/{p} = 2^(32-{p}) = {1 << (32 - p):,} addresses - 5 reserved "
                        f"= {high:,} usable, which covers {hosts}. One size smaller, "
                        f"/{p + 1}, leaves only {(1 << (31 - p)) - 5:,} usable - not "
                        "enough. Bigger prefix number = smaller subnet.")
        return go

    if kind == "inside":
        p = random.randint(22, 28)
        size = 1 << (32 - p)
        net = _rand_net(p)
        cidr = f"{_int_to_ip(net)}/{p}"
        inside = random.random() < 0.5
        if inside:
            ip = net + random.randrange(size)
        else:
            # A neighboring block is guaranteed to mask to a different network.
            ip = net + random.choice([-2, -1, 1, 2]) * size + random.randrange(size)
        ip_s = _int_to_ip(ip)

        def go():
            print(wrap(f"Is {C.BOLD}{ip_s}{C.RESET} inside the subnet "
                       f"{C.BOLD}{cidr}{C.RESET}?  (y/n)"))
            ans = get_input("  y/n: ").lower()
            ok = ans.startswith("y") == inside
            masked = ip & (0xFFFFFFFF ^ (size - 1))
            verdict = "INSIDE" if inside else "OUTSIDE"
            return ok, (f"{cidr} spans {_int_to_ip(net)} - {_int_to_ip(net + size - 1)} "
                        f"({size:,} addresses). Zeroing the {32 - p} host bits of "
                        f"{ip_s} gives network {_int_to_ip(masked)}, which "
                        f"{'matches' if inside else 'does not match'} -> {verdict}.")
        return go

    if kind == "first":
        p = random.randint(24, 29)
        net = _rand_net(p)
        first = net + 4

        def go():
            print(wrap(f"What is the FIRST address you can actually assign to a VM "
                       f"in {C.BOLD}{_int_to_ip(net)}/{p}{C.RESET}?"))
            ans = get_input("  IP: ").strip()
            ok = ans == _int_to_ip(first)
            return ok, (f"Azure takes {_int_to_ip(net)} (network), "
                        f"{_int_to_ip(net + 1)} (default gateway), and "
                        f"{_int_to_ip(net + 2)}-{_int_to_ip(net + 3)} (Azure DNS). "
                        f"First usable = network + 4 = {_int_to_ip(first)}.")
        return go

    # reserved-address recall
    variant = random.choice(["count", "minimum", "which"])
    if variant == "count":
        def go():
            print(wrap("Azure reserves how many IP addresses in EVERY subnet?"))
            val = _parse_int(get_input("  Count: "))
            ok = val == 5
            return ok, ("5 per subnet: .0 network address, .1 default gateway, "
                        ".2 and .3 Azure DNS, and the last address (broadcast). "
                        "That's why usable = 2^(32-N) - 5.")
        return go

    if variant == "minimum":
        def go():
            print(wrap("What is the SMALLEST subnet Azure lets you create? "
                       "(answer as /N)"))
            val = _parse_int(get_input("  Prefix: "))
            ok = val == 29
            return ok, ("/29 is the minimum: 8 addresses - 5 reserved = 3 usable. "
                        "A /30 has only 4 addresses - fewer than the 5 Azure "
                        "reserves - so it cannot exist in a VNet.")
        return go

    net = _rand_net(24)
    offset, role, accepted = random.choice(RESERVED_ROLES)
    ip_s = _int_to_ip(net + offset)

    def go():
        print(wrap(f"In subnet {C.BOLD}{_int_to_ip(net)}/24{C.RESET}, Azure "
                   f"reserves {C.BOLD}{ip_s}{C.RESET} for what purpose? "
                   "(network / gateway / dns / broadcast)"))
        ans = normalize(get_input("  Purpose: "))
        ok = _fuzzy_in(ans, accepted, cutoff=0.8)
        return ok, (f"{ip_s} is {role}. Full reserved set in a /24: .0 network, "
                    ".1 default gateway, .2-.3 Azure DNS, .255 broadcast.")
    return go


# --------------------------------------------------- level 2: RBAC & scope --

# (role name, what it grants, accepted answers)
ROLES = [
    ("Owner",
     "full access to all resources AND can assign roles to others",
     ["owner"]),
    ("Contributor",
     "create and manage all resource types, but CANNOT grant access or assign roles",
     ["contributor"]),
    ("Reader",
     "view all resources; change nothing",
     ["reader"]),
    ("User Access Administrator",
     "manage user access to Azure resources (role assignments) - nothing else",
     ["user access administrator", "user access admin", "uaa"]),
    ("Virtual Machine Contributor",
     "create and manage virtual machines (restart, resize, delete) - not the VNet or storage they use, and no sign-in rights",
     ["virtual machine contributor", "vm contributor"]),
    ("Network Contributor",
     "create and manage all networking resources (VNets, subnets, NSGs, load balancers)",
     ["network contributor"]),
    ("Storage Blob Data Contributor",
     "read, write, and delete blob containers and blob data (data plane)",
     ["storage blob data contributor", "blob data contributor"]),
    ("Storage Blob Data Reader",
     "read blob containers and blob data only (data plane)",
     ["storage blob data reader", "blob data reader"]),
    ("Backup Contributor",
     "manage backups in a Recovery Services vault, but not delete the vault or grant access",
     ["backup contributor"]),
    ("Monitoring Reader",
     "read all monitoring data (metrics, logs, alerts) without touching resources",
     ["monitoring reader"]),
]

# (task description, least-privileged role)
RBAC_SCENARIOS = [
    ("restart, resize, and manage VMs in a resource group - but NOT the virtual "
     "network or storage account they use", "Virtual Machine Contributor"),
    ("grant other people access to a subscription without being able to change "
     "any resources", "User Access Administrator"),
    ("an application must upload and delete blobs in a container",
     "Storage Blob Data Contributor"),
    ("an auditor needs to view every resource's configuration and nothing more",
     "Reader"),
    ("a reporting job only reads blob data - no writes, no account keys",
     "Storage Blob Data Reader"),
    ("manage VNets, subnets, and NSGs - and nothing outside networking",
     "Network Contributor"),
    ("enable and manage VM backups in a Recovery Services vault without being "
     "able to delete the vault", "Backup Contributor"),
    ("a NOC operator reads metrics, logs, and alerts but must not modify anything",
     "Monitoring Reader"),
    ("create and manage every type of resource, but must NOT be able to grant "
     "access to others", "Contributor"),
    ("full control of the resource group, including assigning roles to teammates",
     "Owner"),
]

# (question, answer_key yes/no, explanation)
RBAC_FACTS = [
    ("A role assigned at the subscription scope applies to every resource group "
     "and resource below it.", "yes",
     "RBAC assignments are inherited by all child scopes: management group > "
     "subscription > resource group > resource."),
    ("The Contributor role can create role assignments for other users.", "no",
     "Contributor manages resources but lacks Microsoft.Authorization/"
     "roleAssignments/write - granting access needs Owner or User Access "
     "Administrator."),
    ("A user with Reader at the subscription and Contributor on one resource "
     "group is effectively a Contributor inside that resource group.", "yes",
     "RBAC is additive: your effective permissions are the union of every "
     "assignment at every scope."),
    ("A ReadOnly lock stops even an Owner from deleting the locked resource.", "yes",
     "Locks apply regardless of RBAC. The Owner must delete the lock first "
     "(lock management itself requires Owner or User Access Administrator)."),
    ("Azure Policy is replaced by RBAC - you only need one of the two.", "no",
     "They answer different questions: RBAC controls WHO can do what; Policy "
     "controls WHAT resources are allowed to look like. Use both together."),
    ("An Entra Global Administrator automatically has access to manage all Azure "
     "resources in the tenant's subscriptions.", "no",
     "Entra roles and Azure RBAC are separate systems. A Global Admin must "
     "'elevate access' to gain User Access Administrator at root scope."),
    ("Deny assignments override role assignments that would otherwise allow an "
     "action.", "yes",
     "Deny assignments (created via managed apps/Blueprints, not directly) "
     "always take precedence over allows."),
    ("You can assign an Azure role to a group instead of to individual users.", "yes",
     "Best practice: assign roles to groups so access follows membership and "
     "there are fewer assignments to manage."),
    ("If no built-in role fits, you can create a custom role with exactly the "
     "actions you need.", "yes",
     "Custom roles combine Actions/NotActions/DataActions and can be assigned "
     "at management group, subscription, or resource group scope."),
    ("Deleting a role assignment made at the subscription also removes the "
     "access it was granting inside child resource groups.", "yes",
     "Inherited access only exists through the parent assignment - remove it "
     "and the inheritance disappears everywhere below."),
    ("The built-in Reader role lets you download the data inside a blob "
     "container.", "no",
     "Reader is a control-plane role - it sees the resource, not the data. "
     "Reading blob content needs a data-plane role like Storage Blob Data "
     "Reader (or a key/SAS)."),
    ("Azure roles can be assigned at the management group scope so they apply "
     "to many subscriptions at once.", "yes",
     "Management group is the broadest assignable scope - handy for org-wide "
     "Reader or a platform team's Owner rights."),
]

SCOPES = ["management group", "subscription", "resource group", "resource"]


def _l2_question():
    kind = random.choice(["role", "role", "fact", "fact", "order"])

    if kind == "role":
        task, role_name = random.choice(RBAC_SCENARIOS)
        grants, accepted = next((g, a) for r, g, a in ROLES if r == role_name)

        def go():
            print(wrap(f"Which LEAST-PRIVILEGED built-in role fits: "
                       f"{C.BOLD}{task}{C.RESET}?"))
            ans = normalize(get_input("  Role: "))
            ok = _fuzzy_in(ans, accepted)
            return ok, (f"{role_name} - grants {grants}. Least privilege: pick "
                        "the narrowest built-in role that still covers the task.")
        return go

    if kind == "order":
        shuffled = SCOPES[:]
        while shuffled == SCOPES:
            random.shuffle(shuffled)

        def go():
            print(wrap("Order these RBAC scopes from TOP (broadest) to BOTTOM "
                       "(most specific):"))
            for i, item in enumerate(shuffled, 1):
                print(f"    {i}. {item}")
            raw = get_input("  Order (e.g. '3 1 4 2'): ").replace(",", " ").split()
            try:
                seq = [shuffled[int(x) - 1] for x in raw]
            except (ValueError, IndexError):
                seq = None
            ok = seq == SCOPES
            return ok, ("Top to bottom: management group > subscription > "
                        "resource group > resource. Assignments made high are "
                        "inherited by everything beneath.")
        return go

    q, key, why = random.choice(RBAC_FACTS)

    def go():
        print(wrap(q + "  (y/n)"))
        ans = get_input("  y/n: ").lower()
        ok = ans.startswith("y") == (key == "yes")
        return ok, f"Answer: {key.upper()}. {why}"
    return go


# ------------------------------------------------ level 3: NSG evaluation ---

NSG_PORTS = [22, 80, 443, 3389, 1433]
PORT_NAMES = {22: "SSH", 80: "HTTP", 443: "HTTPS", 3389: "RDP", 1433: "SQL"}

# (priority, name, source, port or None=Any, action)
NSG_DEFAULTS = [
    (65000, "AllowVnetInBound", "VirtualNetwork", None, "allow"),
    (65001, "AllowAzureLoadBalancerInBound", "AzureLoadBalancer", None, "allow"),
    (65500, "DenyAllInBound", "Any", None, "deny"),
]

NSG_FACTS = [
    ("For INBOUND traffic to a VM, is the subnet NSG evaluated before the NIC "
     "NSG?", "yes",
     "Inbound order: subnet NSG first, then NIC NSG. (Outbound is the reverse: "
     "NIC first, then subnet.)"),
    ("If a subnet NSG allows inbound port 443 but the NIC NSG denies it, does "
     "the traffic reach the VM?", "no",
     "BOTH NSGs must allow the flow - a deny at either level kills it."),
    ("Does a LOWER priority number mean the rule is evaluated FIRST?", "yes",
     "Rules run in ascending priority order (100 before 4096 before 65500); "
     "processing stops at the first match."),
    ("Can you delete the three default NSG rules (65000/65001/65500)?", "no",
     "Default rules cannot be deleted - you can only override them with custom "
     "rules at a lower (stronger) priority number."),
    ("Do Azure Load Balancer health probes come from 168.63.129.16?", "yes",
     "168.63.129.16 is Azure's virtual public IP for health probes and DHCP/DNS "
     "- the default AllowAzureLoadBalancerInBound rule admits it."),
    ("Are NSG rules stateful - is return traffic for an allowed flow "
     "automatically permitted?", "yes",
     "NSGs track flows: if the request was allowed, the response is allowed "
     "without a matching rule in the other direction."),
    ("Can one NSG be associated with multiple subnets?", "yes",
     "An NSG is a standalone resource - associate it with many subnets and NICs "
     "to reuse the same rule set."),
    ("Can an application security group (ASG) be the source or destination of "
     "an NSG rule?", "yes",
     "ASGs group NICs by workload so rules can say 'web-servers -> db-servers' "
     "instead of listing IPs."),
    ("Once a rule matches a flow, does Azure keep checking the remaining "
     "lower-priority rules?", "no",
     "First match wins - evaluation stops at the first rule whose "
     "source/port/protocol matches."),
]


def _nsg_eval(rules, source, port):
    """First-match-wins evaluation. Returns (priority, name, action)."""
    for prio, name, src, p, action in sorted(rules):
        if src == "VirtualNetwork" and source != "VNet":
            continue
        if src == "AzureLoadBalancer":
            continue  # our generated flows never come from the LB probe IP
        if p is not None and p != port:
            continue
        return prio, name, action
    return 65500, "DenyAllInBound", "deny"  # unreachable: DenyAll matches all


def _l3_question():
    kind = random.choice(["table", "table", "table", "fact", "fact"])

    if kind == "fact":
        q, key, why = random.choice(NSG_FACTS)

        def go():
            print(wrap(q + "  (y/n)"))
            ans = get_input("  y/n: ").lower()
            ok = ans.startswith("y") == (key == "yes")
            return ok, f"Answer: {key.upper()}. {why}"
        return go

    n = random.randint(2, 3)
    custom = []
    for pr in sorted(random.sample(range(100, 4097), n)):
        port = random.choice(NSG_PORTS)
        action = random.choice(["allow", "deny"])
        custom.append((pr, f"{action.title()}-{PORT_NAMES[port]}", "Any", port, action))
    rules = custom + NSG_DEFAULTS
    source = random.choice(["Internet", "VNet"])
    dport = random.choice(NSG_PORTS)
    wprio, wname, waction = _nsg_eval(rules, source, dport)

    def go():
        print(wrap("An NSG has these INBOUND rules:"))
        print(C.DIM + f"    {'Pri':<8}{'Name':<32}{'Source':<19}{'Port':<7}Action"
              + C.RESET)
        for pr, name, src, p, action in rules:
            pstr = str(p) if p is not None else "Any"
            print(f"    {pr:<8}{name:<32}{src:<19}{pstr:<7}{action.title()}")
        print(wrap(f"Flow: source = {C.BOLD}{source}{C.RESET}, destination port "
                   f"= {C.BOLD}{dport} ({PORT_NAMES[dport]}){C.RESET}. "
                   "Allowed or denied?"))
        ans = normalize(get_input("  allow/deny: "))
        ok = ans.startswith("a") == (waction == "allow")
        return ok, (f"Rules run in ascending priority; the FIRST match wins. "
                    f"Winning rule here: {wprio} {wname} -> {waction.upper()}. "
                    "Remember: VNet-sourced traffic can match 65000 "
                    "AllowVnetInBound, while Internet traffic that matches no "
                    "custom rule falls through to 65500 DenyAllInBound.")
    return go


# --------------------------------------------- level 4: HA & redundancy -----

# (configuration, SLA % as string)
VM_SLA = [
    ("a single VM using Premium SSD or Ultra Disk", "99.9"),
    ("two or more VMs in an availability set", "99.95"),
    ("two or more VMs spread across availability zones", "99.99"),
]

REDUNDANCY = [
    ("LRS", "Locally Redundant Storage", 3,
     "3 synchronous copies in ONE datacenter - cheapest, survives drive/rack failure only"),
    ("ZRS", "Zone-Redundant Storage", 3,
     "3 synchronous copies across THREE availability zones in the primary region"),
    ("GRS", "Geo-Redundant Storage", 6,
     "LRS in the primary region + 3 more async copies in the paired secondary region"),
    ("GZRS", "Geo-Zone-Redundant Storage", 6,
     "ZRS in the primary region + 3 more async copies in the paired secondary region"),
]

TIER_DAYS = [("cool", 30), ("cold", 90), ("archive", 180)]

TIER_SCENARIOS = [
    ("data the app reads and writes every day", "hot"),
    ("data kept online but rarely read, stored at least 30 days", "cool"),
    ("data still online but almost never read, stored at least 90 days", "cold"),
    ("compliance archives that can wait hours to rehydrate, kept at least 180 days",
     "archive"),
]


def _l4_question():
    kind = random.choice(["sla", "downtime", "domains", "domains",
                          "copies", "pick_redundancy", "tier_days", "pick_tier"])

    if kind == "sla":
        config, sla_s = random.choice(VM_SLA)

        def go():
            print(wrap(f"What is the VM uptime SLA for {C.BOLD}{config}{C.RESET}? "
                       "(as a percentage)"))
            val = _parse_float(get_input("  SLA %: "))
            ok = val is not None and abs(val - float(sla_s)) < 1e-9
            return ok, (f"{config}: {sla_s}%. The ladder: single Premium-SSD VM "
                        "99.9% < availability set 99.95% < availability zones "
                        "99.99%. More infrastructure spread = more nines.")
        return go

    if kind == "downtime":
        config, sla_s = random.choice(VM_SLA)
        sla = float(sla_s)
        pct = round(100 - sla, 3)
        minutes = round(43200 * pct / 100, 3)

        def go():
            print(wrap(f"A deployment carries the {C.BOLD}{sla_s}%{C.RESET} SLA "
                       f"({config}). What is the maximum downtime per 30-day "
                       "month, in MINUTES? (within 5% counts)"))
            val = _parse_float(get_input("  Minutes: "))
            ok = val is not None and abs(val - minutes) <= max(0.05 * minutes, 0.05)
            return ok, (f"{sla_s}% up = {pct:g}% down. 30 days = 43,200 minutes; "
                        f"{pct:g}% of 43,200 = {minutes:g} minutes/month.")
        return go

    if kind == "domains":
        d, dlabel, event, verb = random.choice([
            (3, "fault domains", "one fault domain's hardware fails", "go down"),
            (5, "update domains",
             "one update domain is rebooted during planned maintenance", "reboot"),
        ])
        n = random.randint(d + 1, 20)
        worst = math.ceil(n / d)
        counts = [n // d + (1 if i < n % d else 0) for i in range(d)]
        dist = "+".join(str(c) for c in counts)
        variant = random.choice(["down", "up"])

        if variant == "down":
            def go():
                print(wrap(f"You place {C.BOLD}{n} VMs{C.RESET} in an availability "
                           f"set with {C.BOLD}{d} {dlabel}{C.RESET} (round-robin). "
                           f"If {event}, AT MOST how many VMs {verb} at once?"))
                val = _parse_int(get_input("  VMs: "))
                ok = val == worst
                return ok, (f"{n} VMs round-robin over {d} {dlabel} = {dist}. The "
                            f"fullest domain holds ceil({n}/{d}) = {worst}, so at "
                            f"most {worst} are affected while {n - worst} keep "
                            "running.")
            return go

        def go():
            print(wrap(f"You place {C.BOLD}{n} VMs{C.RESET} in an availability "
                       f"set with {C.BOLD}{d} {dlabel}{C.RESET} (round-robin). "
                       f"If {event}, how many VMs are GUARANTEED to stay up?"))
            val = _parse_int(get_input("  VMs: "))
            ok = val == n - worst
            return ok, (f"{n} VMs round-robin over {d} {dlabel} = {dist}. Worst "
                        f"case loses the fullest domain: ceil({n}/{d}) = {worst} "
                        f"down, {n} - {worst} = {n - worst} still running.")
        return go

    if kind == "copies":
        abbr, full, copies, why = random.choice(REDUNDANCY)

        def go():
            print(wrap(f"How many total copies of your data does "
                       f"{C.BOLD}{full} ({abbr}){C.RESET} keep?"))
            val = _parse_int(get_input("  Copies: "))
            ok = val == copies
            return ok, f"{abbr} = {copies} copies. {why}"
        return go

    if kind == "pick_redundancy":
        scenarios = [
            ("the cheapest redundancy, no protection needed beyond one datacenter", "LRS"),
            ("survive a whole datacenter (zone) failure, but data must stay in one region", "ZRS"),
            ("survive the loss of an entire region, at the lowest cost that does so", "GRS"),
            ("survive both a zone failure AND a regional disaster", "GZRS"),
        ]
        want, expected = random.choice(scenarios)

        def go():
            print(wrap(f"Which storage redundancy option fits: "
                       f"{C.BOLD}{want}{C.RESET}? (LRS / ZRS / GRS / GZRS)"))
            ans = normalize(get_input("  Option: ")).replace(" ", "")
            ok = ans == expected.lower()
            why = next(r[3] for r in REDUNDANCY if r[0] == expected)
            return ok, f"{expected}: {why}"
        return go

    if kind == "tier_days":
        tier, days = random.choice(TIER_DAYS)

        def go():
            print(wrap(f"Blobs in the {C.BOLD}{tier.upper()}{C.RESET} tier should "
                       "stay there at least how many DAYS to avoid the "
                       "early-deletion charge?"))
            val = _parse_int(get_input("  Days: "))
            ok = val == days
            return ok, (f"{tier.title()} = {days} days minimum. The ladder: cool "
                        "30 / cold 90 / archive 180. Hot has no minimum; archive "
                        "is offline and takes hours to rehydrate.")
        return go

    want, expected = random.choice(TIER_SCENARIOS)

    def go():
        print(wrap(f"Which blob access tier fits: {C.BOLD}{want}{C.RESET}? "
                   "(hot / cool / cold / archive)"))
        ans = normalize(get_input("  Tier: "))
        ok = ans == expected
        return ok, (f"{expected.title()} tier. Minimum-days ladder: cool 30 / "
                    "cold 90 / archive 180; hot has no minimum. Cooler tier = "
                    "cheaper storage but pricier, slower access.")
    return go


def _gym_question(level):
    """Returns go() -> (bool, explanation_str)."""
    if level == 1:
        return _l1_question()
    if level == 2:
        return _l2_question()
    if level == 3:
        return _l3_question()
    return _l4_question()


def azure_gym():
    banner("AZURE GYM", C.MAGENTA)
    print("""
  1) Level 1 - Subnetting & CIDR  (usable IPs, right-size prefixes, reserved addresses)
  2) Level 2 - RBAC & scope       (least privilege, inheritance, hierarchy)
  3) Level 3 - NSG evaluation     (priority tables, first match wins, default rules)
  4) Level 4 - HA & redundancy    (VM SLAs, fault/update domains, copies, tiers)
""")
    score, asked = 0, 0
    try:
        while True:
            lvl = get_input("  Level (1-4): ")
            if lvl in ("1", "2", "3", "4"):
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
