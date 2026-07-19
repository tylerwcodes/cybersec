# AZ-900 Acronym List

Microsoft doesn't publish an official acronym appendix the way CompTIA does,
so this list is curated from the AZ-900 "Skills measured" outline and the
Microsoft Learn fundamentals path. Drill these with the **Acronym blitz** mode
in the study games.

| Acronym | Spelled out | Why it matters |
|---|---|---|
| ACI | Azure Container Instances | Run a single container without servers or an orchestrator |
| AKS | Azure Kubernetes Service | Managed Kubernetes for container orchestration |
| API | Application Programming Interface | How programs talk to services (REST APIs, App Service) |
| ARM | Azure Resource Manager | Deployment/management layer behind portal, CLI, PowerShell |
| AVD | Azure Virtual Desktop | Cloud-hosted Windows desktops and apps |
| B2B | Business to Business | Entra External ID: invite partner/guest users |
| B2C | Business to Consumer | Entra External ID: customer-facing app sign-in |
| CapEx | Capital Expenditure | Up-front spend on physical infrastructure (on-prem model) |
| CDN | Content Delivery Network | Cache content close to users |
| CLI | Command-Line Interface | Azure CLI (`az` commands), cross-platform |
| CSPM | Cloud Security Posture Management | What Defender for Cloud provides (secure score) |
| DDoS | Distributed Denial of Service | Attack type; Azure DDoS Protection defends against it |
| DNS | Domain Name System | Azure DNS hosts zones and answers queries |
| FIDO2 | Fast Identity Online 2 | Passwordless hardware security keys |
| GRS | Geo-Redundant Storage | 3 local copies + 3 copies in a secondary region (6 total) |
| GZRS | Geo-Zone-Redundant Storage | ZRS in primary region + LRS in secondary (6 total) |
| HTTPS | Hypertext Transfer Protocol Secure | Encrypted web traffic (TLS) |
| IaaS | Infrastructure as a Service | VMs, storage, networks — you manage OS and up |
| IaC | Infrastructure as Code | Declarative deployments: ARM templates, Bicep |
| IoT | Internet of Things | Fleet of connected devices |
| JSON | JavaScript Object Notation | The format of ARM templates |
| KQL | Kusto Query Language | Query language for Log Analytics |
| LRS | Locally Redundant Storage | 3 copies in one datacenter — cheapest option |
| MFA | Multifactor Authentication | Something you know + have + are |
| NFS | Network File System | Protocol option for Azure Files (Linux) |
| NIC | Network Interface Card | Required resource for every VM |
| NSG | Network Security Group | Allow/deny traffic rules on subnets and NICs |
| OpEx | Operational Expenditure | Pay-as-you-go spending (cloud consumption model) |
| OS | Operating System | The IaaS/PaaS dividing line: who patches it? |
| P2S | Point-to-Site | VPN from a single device to a VNet |
| PaaS | Platform as a Service | Provider manages OS/runtime; you bring code + data |
| RA-GRS | Read-Access Geo-Redundant Storage | GRS + read access to the secondary region |
| RA-GZRS | Read-Access Geo-Zone-Redundant Storage | GZRS + read access to the secondary region |
| RBAC | Role-Based Access Control | Roles (Owner/Contributor/Reader) assigned at a scope |
| RDP | Remote Desktop Protocol | Admin access to Windows VMs (port 3389) |
| REST | Representational State Transfer | API style used by ARM and most Azure services |
| S2S | Site-to-Site | VPN connecting an on-prem network to a VNet |
| SaaS | Software as a Service | Finished app you just use (Microsoft 365) |
| SLA | Service-Level Agreement | Microsoft's uptime guarantee, e.g. 99.9% |
| SMB | Server Message Block | Protocol for Azure Files shares (Windows) |
| SQL | Structured Query Language | Azure SQL Database (PaaS relational DB) |
| SSH | Secure Shell | Admin access to Linux VMs (port 22) |
| SSO | Single Sign-On | One sign-in for many applications (Entra ID) |
| TCO | Total Cost of Ownership | Calculator comparing on-prem cost vs. Azure |
| TLS | Transport Layer Security | Encryption in transit |
| VM | Virtual Machine | The core IaaS compute unit |
| VMSS | Virtual Machine Scale Sets | Auto-scaling group of identical VMs |
| VNet | Virtual Network | Your private network in Azure |
| VPN | Virtual Private Network | Encrypted tunnel over the public Internet |
| ZRS | Zone-Redundant Storage | 3 copies across 3 availability zones |

## Name changes worth knowing

The exam and Microsoft Learn now use new names for several familiar products —
older practice material may use the old ones:

| Old name | Current name |
|---|---|
| Azure Active Directory (Azure AD) | **Microsoft Entra ID** |
| Azure AD Domain Services | **Microsoft Entra Domain Services** |
| Azure AD B2B / B2C | **Microsoft Entra External ID** (B2B collaboration / customer identities) |
| Azure Cost Management + Billing | **Microsoft Cost Management** |
| Azure Security Center | **Microsoft Defender for Cloud** |
| Azure Sentinel | **Microsoft Sentinel** |
