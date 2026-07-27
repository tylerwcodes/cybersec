# CompTIA Security+ SY0-701 — Complete Study Guide

A full-coverage study guide built directly from the official CompTIA SY0-701
exam objectives. Every objective, bullet, and sub-bullet from the objectives
document has a dedicated section.

## Exam facts

| | |
|---|---|
| Exam code | SY0-701 |
| Questions | Maximum of 90 (multiple-choice + performance-based) |
| Length | 90 minutes |
| Passing score | 750 (on a scale of 100–900) |
| Recommended experience | CompTIA Network+ and 2 years in a security/systems admin role |

## Domain weights

| Domain | Weight | Chapters |
|---|---|---|
| 1.0 General Security Concepts | 12% | 4 |
| 2.0 Threats, Vulnerabilities, and Mitigations | 22% | 5 |
| 3.0 Security Architecture | 18% | 4 |
| 4.0 Security Operations | **28%** | 9 |
| 5.0 Security Program Management and Oversight | 20% | 6 |

Security Operations is the single biggest domain — nine objectives of hands-on
"given a scenario" material. Together with Threats (D2) it's exactly half the
exam, and both are scenario-heavy: expect to *apply* concepts, not just define
them.

## Chapters

### Domain 1 — General Security Concepts (12%)
- [1.1 Security Controls](domain-1-general-security-concepts/1.1-security-controls.md)
- [1.2 Fundamental Security Concepts](domain-1-general-security-concepts/1.2-fundamental-security-concepts.md)
- [1.3 Change Management](domain-1-general-security-concepts/1.3-change-management.md)
- [1.4 Cryptographic Solutions](domain-1-general-security-concepts/1.4-cryptographic-solutions.md)

### Domain 2 — Threats, Vulnerabilities, and Mitigations (22%)
- [2.1 Threat Actors & Motivations](domain-2-threats-vulnerabilities-mitigations/2.1-threat-actors-motivations.md)
- [2.2 Threat Vectors & Attack Surfaces](domain-2-threats-vulnerabilities-mitigations/2.2-threat-vectors-attack-surfaces.md)
- [2.3 Types of Vulnerabilities](domain-2-threats-vulnerabilities-mitigations/2.3-vulnerability-types.md)
- [2.4 Indicators of Malicious Activity](domain-2-threats-vulnerabilities-mitigations/2.4-malicious-activity-indicators.md)
- [2.5 Mitigation Techniques](domain-2-threats-vulnerabilities-mitigations/2.5-mitigation-techniques.md)

### Domain 3 — Security Architecture (18%)
- [3.1 Architecture Models](domain-3-security-architecture/3.1-architecture-models.md)
- [3.2 Securing Enterprise Infrastructure](domain-3-security-architecture/3.2-securing-enterprise-infrastructure.md)
- [3.3 Data Protection](domain-3-security-architecture/3.3-data-protection.md)
- [3.4 Resilience & Recovery](domain-3-security-architecture/3.4-resilience-recovery.md)

### Domain 4 — Security Operations (28%)
- [4.1 Securing Computing Resources](domain-4-security-operations/4.1-securing-computing-resources.md)
- [4.2 Asset Management](domain-4-security-operations/4.2-asset-management.md)
- [4.3 Vulnerability Management](domain-4-security-operations/4.3-vulnerability-management.md)
- [4.4 Alerting & Monitoring](domain-4-security-operations/4.4-alerting-monitoring.md)
- [4.5 Enterprise Security Capabilities](domain-4-security-operations/4.5-enterprise-security-capabilities.md)
- [4.6 Identity & Access Management](domain-4-security-operations/4.6-identity-access-management.md)
- [4.7 Automation & Orchestration](domain-4-security-operations/4.7-automation-orchestration.md)
- [4.8 Incident Response](domain-4-security-operations/4.8-incident-response.md)
- [4.9 Investigation Data Sources](domain-4-security-operations/4.9-investigation-data-sources.md)

### Domain 5 — Security Program Management and Oversight (20%)
- [5.1 Security Governance](domain-5-security-program-management/5.1-security-governance.md)
- [5.2 Risk Management](domain-5-security-program-management/5.2-risk-management.md)
- [5.3 Third-Party Risk](domain-5-security-program-management/5.3-third-party-risk.md)
- [5.4 Security Compliance](domain-5-security-program-management/5.4-security-compliance.md)
- [5.5 Audits & Assessments](domain-5-security-program-management/5.5-audits-assessments.md)
- [5.6 Security Awareness](domain-5-security-program-management/5.6-security-awareness.md)

### Reference
- [Official Acronym List](acronyms.md) — all acronyms from the objectives document

## The study games

A terminal study-game suite lives in `../study-games/`. Launch it with:

```bash
cd ../study-games
python3 secplus.py
```

Every chapter here has a matching game topic with quizzes, flashcards, and
term-matching. There are also global modes:

- **Exam simulator** — 90 questions weighted exactly like the real exam, timed
- **Control classifier gym** — objective 1.1 drilled to reflex: category and type
- **Port & protocol blitz** — ports forward and reverse, plus "name the secure replacement"
- **Acronym blitz** — the full official acronym list
- **Review missed** — every question you've ever gotten wrong, until you clear it
- **Stats** — accuracy per topic and your three weakest areas

Progress persists between sessions in `study-games/.progress.json`.

## Suggested study plan

1. **Read one chapter, then play its topic games immediately.** Retrieval right
   after reading is what makes it stick.
2. **Hit the Control classifier gym until it's automatic.** Objective 1.1 is
   the vocabulary the rest of the exam is written in — "which type of control
   is this?" hides inside scenario questions from every domain.
3. **Run Port & protocol blitz and Acronym blitz as warm-ups** at the start of
   each session. The secure-replacement questions (Telnet→SSH, LDAP→LDAPS,
   SNMP→SNMPv3) are near-guaranteed exam material via objective 4.5.
4. **Clear your review pile weekly** (R in the main menu). A question isn't
   "done" until you've answered it correctly after missing it.
5. **Take the exam simulator when topic accuracy is ≥80% across the board.**
   Score 80%+ on two consecutive simulations before booking the real exam.
6. Exam-day mechanics: flag and skip anything slow, do performance-based
   questions last if they bog you down, and remember there's no penalty for
   guessing — never leave a blank.
