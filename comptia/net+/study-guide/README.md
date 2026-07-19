# CompTIA Network+ N10-009 — Complete Study Guide

A full-coverage study guide built directly from the official CompTIA N10-009
exam objectives (Version 4.0). Every objective, bullet, and sub-bullet from the
objectives document has a dedicated section.

## Exam facts

| | |
|---|---|
| Exam code | N10-009 |
| Questions | Maximum of 90 (multiple-choice + performance-based) |
| Length | 90 minutes |
| Passing score | 720 (on a scale of 100–900) |
| Recommended experience | 9–12 months in IT networking |

## Domain weights

| Domain | Weight | Chapters |
|---|---|---|
| 1.0 Networking Concepts | 23% | 8 |
| 2.0 Network Implementation | 20% | 4 |
| 3.0 Network Operations | 19% | 5 |
| 4.0 Network Security | 14% | 3 |
| 5.0 Network Troubleshooting | **24%** | 5 |

Troubleshooting is the single biggest domain — and it re-tests everything else
in scenario form. Concepts (D1) plus Troubleshooting (D5) are nearly half the
exam.

## Chapters

### Domain 1 — Networking Concepts (23%)
- [1.1 OSI Model](domain-1-networking-concepts/1.1-osi-model.md)
- [1.2 Appliances, Applications & Functions](domain-1-networking-concepts/1.2-appliances-applications-functions.md)
- [1.3 Cloud Concepts & Connectivity](domain-1-networking-concepts/1.3-cloud-concepts.md)
- [1.4 Ports, Protocols, Services & Traffic Types](domain-1-networking-concepts/1.4-ports-protocols-traffic.md)
- [1.5 Transmission Media & Transceivers](domain-1-networking-concepts/1.5-transmission-media-transceivers.md)
- [1.6 Topologies, Architectures & Types](domain-1-networking-concepts/1.6-topologies-architectures.md)
- [1.7 IPv4 Network Addressing](domain-1-networking-concepts/1.7-ipv4-addressing.md)
- [1.8 Modern Network Environments](domain-1-networking-concepts/1.8-modern-network-environments.md)

### Domain 2 — Network Implementation (20%)
- [2.1 Routing Technologies](domain-2-network-implementation/2.1-routing-technologies.md)
- [2.2 Switching Technologies](domain-2-network-implementation/2.2-switching-technologies.md)
- [2.3 Wireless Devices & Technologies](domain-2-network-implementation/2.3-wireless-devices-technologies.md)
- [2.4 Physical Installations](domain-2-network-implementation/2.4-physical-installations.md)

### Domain 3 — Network Operations (19%)
- [3.1 Organizational Processes & Procedures](domain-3-network-operations/3.1-processes-procedures.md)
- [3.2 Network Monitoring](domain-3-network-operations/3.2-network-monitoring.md)
- [3.3 Disaster Recovery](domain-3-network-operations/3.3-disaster-recovery.md)
- [3.4 IPv4/IPv6 Network Services (DHCP, DNS, NTP)](domain-3-network-operations/3.4-ipv4-ipv6-network-services.md)
- [3.5 Network Access & Management Methods](domain-3-network-operations/3.5-access-management-methods.md)

### Domain 4 — Network Security (14%)
- [4.1 Security Concepts](domain-4-network-security/4.1-security-concepts.md)
- [4.2 Attacks & Their Impact](domain-4-network-security/4.2-attacks.md)
- [4.3 Defense Techniques & Solutions](domain-4-network-security/4.3-defense-techniques.md)

### Domain 5 — Network Troubleshooting (24%)
- [5.1 Troubleshooting Methodology](domain-5-network-troubleshooting/5.1-troubleshooting-methodology.md)
- [5.2 Cabling & Physical Interface Issues](domain-5-network-troubleshooting/5.2-cabling-physical-issues.md)
- [5.3 Network Service Issues](domain-5-network-troubleshooting/5.3-network-services-issues.md)
- [5.4 Performance Issues](domain-5-network-troubleshooting/5.4-performance-issues.md)
- [5.5 Tools & Protocols](domain-5-network-troubleshooting/5.5-tools-protocols.md)

### Reference
- [Official Acronym List](acronyms.md) — all acronyms from the objectives document

## The study games

A terminal study-game suite lives in `../study-games/`. Launch it with:

```bash
cd ../study-games
python3 netplus.py
```

Every chapter here has a matching game topic with quizzes, flashcards, and
term-matching. There are also global modes:

- **Exam simulator** — 90 questions weighted exactly like the real exam, timed
- **Subnetting gym** — infinitely generated subnetting problems, 3 levels
- **Port blitz** — the official port table, forward and reverse, with streaks
- **Acronym blitz** — the full official acronym list
- **Review missed** — every question you've ever gotten wrong, until you clear it
- **Stats** — accuracy per topic and your three weakest areas

Progress persists between sessions in `study-games/.progress.json`.

## Suggested study plan

1. **Read one chapter, then play its topic games immediately.** Retrieval right
   after reading is what makes it stick.
2. **Hit the Subnetting gym daily.** Subnetting appears throughout the exam and
   speed matters on the performance-based questions — aim for under 30 seconds
   per problem at Level 2.
3. **Run Port blitz and Acronym blitz as warm-ups** at the start of each session.
4. **Clear your review pile weekly** (R in the main menu). A question isn't
   "done" until you've answered it correctly after missing it.
5. **Take the exam simulator when topic accuracy is ≥80% across the board.**
   Score 80%+ on two consecutive simulations before booking the real exam.
6. Exam-day mechanics: flag and skip anything slow, do performance-based
   questions last if they bog you down, and remember there's no penalty for
   guessing — never leave a blank.
