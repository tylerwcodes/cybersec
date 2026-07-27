# AZ-104 Acronym List

Microsoft doesn't publish an official acronym appendix the way CompTIA does,
so this list is curated from the AZ-104 "Skills measured" outline and the
Microsoft Learn administrator path. It is grouped by exam domain. Drill these
with the **Acronym blitz** mode in the study games.

## Identity and governance

| Acronym | Spelled out | Why it matters |
|---|---|---|
| ABAC | Attribute-Based Access Control | Role assignment *conditions* (e.g. only blobs with a given tag) layered on top of RBAC |
| AU | Administrative Unit | Scope Entra roles to a subset of users/devices (e.g. one department) |
| JIT | Just-in-Time | Time-boxed access: PIM role activation and Defender JIT VM access |
| MFA | Multifactor Authentication | Something you know + have + are; enforced per-user or via Conditional Access |
| PIM | Privileged Identity Management | Eligible (not permanent) role assignments with activation, approval, and audit |
| RBAC | Role-Based Access Control | Roles (Owner/Contributor/Reader) assigned at management group/subscription/RG/resource scope |
| SSO | Single Sign-On | One Entra ID sign-in for many applications |
| SSPR | Self-Service Password Reset | Users reset their own passwords; requires registered auth methods |

## Storage

| Acronym | Spelled out | Why it matters |
|---|---|---|
| ADE | Azure Disk Encryption | BitLocker/dm-crypt *inside* the VM, keys in Key Vault — vs. platform SSE |
| ADLS | Azure Data Lake Storage (Gen2) | Blob storage with hierarchical namespace enabled (at creation, or via one-way upgrade) |
| CMK | Customer-Managed Key | You supply the encryption key from Key Vault instead of Microsoft's |
| GiB | Gibibyte (2^30 bytes) | The unit Azure actually uses for disk and memory sizes |
| GRS | Geo-Redundant Storage | 3 local copies + 3 copies in the paired region (6 total) |
| GZRS | Geo-Zone-Redundant Storage | ZRS in primary region + LRS in secondary (6 total) |
| LRS | Locally Redundant Storage | 3 copies in one datacenter — cheapest, no zone or region protection |
| NFS | Network File System | Azure Files protocol for Linux; requires Premium (FileStorage) account |
| PMK | Platform-Managed Key | Default encryption key, managed by Microsoft — the alternative to CMK |
| RA-GRS | Read-Access Geo-Redundant Storage | GRS + read access to the secondary region |
| RA-GZRS | Read-Access Geo-Zone-Redundant Storage | GZRS + read access to the secondary region |
| SAS | Shared Access Signature | Time-limited, scoped token URL for storage access; service, account, or user-delegation |
| SMB | Server Message Block | Azure Files protocol for Windows (port 445, often blocked by ISPs) |
| SSE | Server-Side Encryption | Automatic at-rest encryption of storage/disks; always on, PMK by default |
| TiB | Tebibyte (2^40 bytes) | File share and disk quotas are stated in TiB (e.g. 100 TiB shares) |
| WORM | Write Once, Read Many | Immutable blob storage: time-based retention and legal holds |
| ZRS | Zone-Redundant Storage | 3 copies across 3 availability zones in one region |

## Compute

| Acronym | Spelled out | Why it matters |
|---|---|---|
| ACA | Azure Container Apps | Serverless containers with scale-to-zero, built on Kubernetes you don't manage |
| ACI | Azure Container Instances | Run a single container/container group fast, no orchestrator |
| ACR | Azure Container Registry | Private registry for container images; Basic/Standard/Premium tiers |
| AKS | Azure Kubernetes Service | Managed Kubernetes; you scale node pools, Microsoft runs the control plane |
| ARM | Azure Resource Manager | Deployment/management layer behind portal, CLI, PowerShell, templates |
| GPU | Graphics Processing Unit | N-series VM sizes for compute/visualization workloads |
| HDD | Hard Disk Drive | Standard HDD disks — cheapest, for dev/test and infrequent access |
| IaC | Infrastructure as Code | Declarative deployments: ARM templates and Bicep, exported or hand-written |
| IOPS | Input/Output Operations Per Second | Disk performance measure; scales with disk SKU and size |
| OS | Operating System | Every VM has exactly one OS disk; you patch it in IaaS |
| SKU | Stock Keeping Unit | The size/tier of almost everything: VMs, disks, public IPs, gateways |
| SSD | Solid-State Drive | Standard SSD vs. Premium SSD (v2) disk tiers; Premium needed for the VM SLA |
| VHD | Virtual Hard Disk | The disk image format; upload a generalized VHD to create custom images |
| VM | Virtual Machine | The core IaaS compute unit you deploy, size, and manage |
| VMSS | Virtual Machine Scale Sets | Identical VMs with autoscale rules (CPU, schedule); flexible vs. uniform |

## Networking

| Acronym | Spelled out | Why it matters |
|---|---|---|
| ASG | Application Security Group | Tag NICs by role and use the tag in NSG rules instead of IP lists |
| BGP | Border Gateway Protocol | Dynamic route exchange for VPN/ExpressRoute; required for active-active |
| CIDR | Classless Inter-Domain Routing | Address-space notation (10.0.0.0/16); Azure reserves 5 IPs per subnet |
| DNAT | Destination Network Address Translation | Azure Firewall rule type that forwards inbound traffic to a private IP |
| DNS | Domain Name System | Azure DNS public zones + private zones with VNet links and auto-registration |
| ER | ExpressRoute | Private circuit to Azure that bypasses the public Internet |
| FQDN | Fully Qualified Domain Name | Full hostname (vm1.contoso.com); used in Firewall application rules |
| ILB | Internal Load Balancer | Load balancer with a private frontend IP — for internal tiers |
| NAT | Network Address Translation | NAT Gateway gives a subnet predictable outbound IPs and fixes SNAT exhaustion |
| NSG | Network Security Group | Allow/deny rules by priority on subnets and NICs; default rules last |
| NVA | Network Virtual Appliance | Third-party firewall/router VM; UDRs steer traffic through it |
| P2S | Point-to-Site | VPN from a single device to a VNet (OpenVPN, IKEv2, SSTP) |
| PIP | Public IP (address) | Standard SKU: static, zone-capable, secure by default; needed for inbound Internet |
| RDP | Remote Desktop Protocol | Admin access to Windows VMs (port 3389); prefer Bastion over open NSGs |
| S2S | Site-to-Site | VPN connecting an on-prem network to a VNet via a VPN gateway |
| SNAT | Source Network Address Translation | Outbound translation via Load Balancer/NAT Gateway; port exhaustion is a classic exam issue |
| SNI | Server Name Indication | Lets Application Gateway host multiple TLS sites on one listener IP |
| SSH | Secure Shell | Admin access to Linux VMs (port 22), password or key pair |
| TLS | Transport Layer Security | Encryption in transit; App Gateway does TLS termination and end-to-end TLS |
| TTL | Time to Live | How long resolvers cache a DNS record — affects failover speed |
| UDR | User-Defined Route | Route table overriding system routes (e.g. 0.0.0.0/0 → firewall) |
| VNet | Virtual Network | Your private network; peering is non-transitive, address spaces can't overlap |
| VPN | Virtual Private Network | Encrypted tunnel over the Internet; gateway SKU sets throughput and BGP support |
| WAF | Web Application Firewall | OWASP rule sets on Application Gateway v2 or Front Door |

### DNS record types

Short names, not true acronyms — but you must know what each one maps to:

| Record | Stands for | Maps |
|---|---|---|
| A | Address | Name → IPv4 address |
| AAAA | Address (IPv6) | Name → IPv6 address |
| CNAME | Canonical Name | Alias name → another name (can't sit at the zone apex) |
| MX | Mail Exchange | Domain → mail servers, with priority |
| NS | Name Server | Zone → its authoritative name servers (delegation) |
| PTR | Pointer | IP → name (reverse lookup) |
| SOA | Start of Authority | Zone metadata: primary server, serial, refresh timers |
| SRV | Service | Service/protocol → host and port (e.g. VoIP, LDAP) |
| TXT | Text | Free text: domain verification, SPF/DKIM entries |

## Monitoring and backup

| Acronym | Spelled out | Why it matters |
|---|---|---|
| AMA | Azure Monitor Agent | Current data-collection agent for VMs — replaces the legacy Log Analytics (MMA/OMS) agent |
| ASR | Azure Site Recovery | Replicates VMs to another region for disaster-recovery failover |
| CRR | Cross-Region Restore | Restore backups in the paired region; requires GRS vault + CRR enabled |
| DCR | Data Collection Rule | Defines what AMA collects and which Log Analytics workspace it lands in |
| GFS | Grandfather-Father-Son | Long-term retention scheme: daily/weekly/monthly/yearly backup points |
| ITSM | IT Service Management | Alert action that creates tickets in tools like ServiceNow |
| KQL | Kusto Query Language | Query language for Log Analytics and log-based alert rules |
| MABS | Microsoft Azure Backup Server | On-prem server backing up VMs/apps (SQL, SharePoint) to Azure |
| MARS | Microsoft Azure Recovery Services (agent) | Agent backing up files/folders/system state from Windows machines |
| RPO | Recovery Point Objective | Max acceptable data loss — how recent the last restore point is |
| RTO | Recovery Time Objective | Max acceptable downtime — how fast you must be running again |
| SIEM | Security Information and Event Management | Where diagnostic/activity logs can be streamed via Event Hubs |

## Name changes worth knowing

The exam and Microsoft Learn now use new names — older practice material may
use the old ones:

| Old name | Current name |
|---|---|
| Azure Active Directory (Azure AD) | **Microsoft Entra ID** |
| Azure AD Domain Services | **Microsoft Entra Domain Services** |
| Log Analytics agent (MMA/OMS agent) | **Azure Monitor Agent (AMA)** — legacy agent retired |
| Azure Security Center | **Microsoft Defender for Cloud** |
