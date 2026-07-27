# Microsoft Azure Administrator AZ-104 — Complete Study Guide

A full-coverage study guide built directly from the official Microsoft AZ-104
"Skills measured" outline. Every objective, bullet, and sub-bullet from the
study guide has a dedicated section.

## Exam facts

| | |
|---|---|
| Exam code | AZ-104 |
| Questions | Typically 40–60 (multiple-choice, drag-and-drop, hot area, case studies) |
| Length | ~100 minutes exam time (~120 minutes seat time) |
| Passing score | 700 (on a scale of 1–1000) |
| Cost | $165 USD |
| Prerequisites | None required, but Microsoft recommends 6+ months of hands-on Azure administration experience |
| Renewal | Certification is valid for 1 year; renew free online via Microsoft Learn |

## Domain weights

| Domain | Weight | Chapters |
|---|---|---|
| 1.0 Manage Azure identities and governance | 20–25% | 3 |
| 2.0 Implement and manage storage | 15–20% | 3 |
| 3.0 Deploy and manage Azure compute resources | 20–25% | 4 |
| 4.0 Implement and manage virtual networking | 15–20% | 3 |
| 5.0 Monitor and maintain Azure resources | 10–15% | 2 |

Identities/governance and compute are the two biggest domains, but AZ-104 is
famous for its networking scenarios — subnetting, NSGs, peering, and load
balancing show up inside questions from *every* domain. Monitoring is the
smallest domain and the easiest place to bank points.

## Chapters

### Domain 1 — Manage Azure Identities and Governance (20–25%)
- [1.1 Entra Users & Groups](domain-1-identities-governance/1.1-entra-users-groups.md)
- [1.2 Azure RBAC](domain-1-identities-governance/1.2-azure-rbac.md)
- [1.3 Subscriptions & Governance](domain-1-identities-governance/1.3-subscriptions-governance.md)

### Domain 2 — Implement and Manage Storage (15–20%)
- [2.1 Storage Access & Security](domain-2-storage/2.1-storage-access.md)
- [2.2 Storage Accounts](domain-2-storage/2.2-storage-accounts.md)
- [2.3 Azure Files & Blob Storage](domain-2-storage/2.3-files-and-blobs.md)

### Domain 3 — Deploy and Manage Azure Compute Resources (20–25%)
- [3.1 ARM Templates & Bicep](domain-3-compute/3.1-arm-bicep.md)
- [3.2 Virtual Machines](domain-3-compute/3.2-virtual-machines.md)
- [3.3 Containers (ACR / ACI / ACA)](domain-3-compute/3.3-containers.md)
- [3.4 App Service](domain-3-compute/3.4-app-service.md)

### Domain 4 — Implement and Manage Virtual Networking (15–20%)
- [4.1 Virtual Networks & Routing](domain-4-networking/4.1-virtual-networks.md)
- [4.2 Secure Network Access](domain-4-networking/4.2-secure-network-access.md)
- [4.3 DNS & Load Balancing](domain-4-networking/4.3-dns-load-balancing.md)

### Domain 5 — Monitor and Maintain Azure Resources (10–15%)
- [5.1 Azure Monitor & Insights](domain-5-monitoring/5.1-monitoring.md)
- [5.2 Backup & Site Recovery](domain-5-monitoring/5.2-backup-recovery.md)

### Reference
- [Acronym List](acronyms.md) — every acronym and short name worth knowing for AZ-104

## The study games

A terminal study-game suite lives in `../study-games/`. Launch it with:

```bash
cd ../study-games
python3 az104.py
```

Every chapter here has a matching game topic with quizzes, flashcards, and
term-matching. There are also global modes:

- **Exam simulator** — 50 questions weighted exactly like the real exam, timed
- **Azure gym** — infinitely generated problems, 4 levels: subnetting & CIDR,
  RBAC & scope, NSG evaluation, HA & redundancy math
- **Service blitz** — 55 admin-level Azure services, name-from-description and
  category questions, with streaks
- **Acronym blitz** — the AZ-104 acronym list, fuzzy-graded
- **Review missed** — every question you've ever gotten wrong, until you clear it
- **Stats** — accuracy per topic and your three weakest areas

Progress persists between sessions in `study-games/.progress.json`.

## Suggested study plan

1. **Read one chapter, then play its topic games immediately.** Retrieval right
   after reading is what makes it stick.
2. **Hit the Azure gym daily.** Subnetting, NSG rule evaluation, and RBAC scope
   questions show up all over the exam in scenario form — they should become
   reflexes, not calculations.
3. **Run Service blitz and Acronym blitz as warm-ups** at the start of each
   session. Many AZ-104 questions reduce to "which service/tier/SKU does X?" —
   the blitz trains exactly that mapping.
4. **Clear your review pile weekly** (R in the main menu). A question isn't
   "done" until you've answered it correctly after missing it.
5. **Take the exam simulator when topic accuracy is ≥80% across the board.**
   Score 80%+ on two consecutive simulations before booking the real exam.
6. Exam-day mechanics: AZ-104 has no penalty for guessing — never leave a
   blank. Case studies come in a separate section you can't return to; budget
   time for them. Read scenario questions for the constraint keywords
   ("minimize cost", "least administrative effort", "without redeploying") —
   they usually eliminate all but one answer.
