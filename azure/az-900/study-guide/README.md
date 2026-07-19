# Microsoft Azure Fundamentals AZ-900 — Complete Study Guide

A full-coverage study guide built directly from the official Microsoft AZ-900
"Skills measured" outline. Every objective, bullet, and sub-bullet from the
study guide has a dedicated section.

## Exam facts

| | |
|---|---|
| Exam code | AZ-900 |
| Questions | Typically 40–60 (multiple-choice, drag-and-drop, hot area) |
| Length | 45 minutes exam time (~65 minutes seat time) |
| Passing score | 700 (on a scale of 1–1000) |
| Cost | $99 USD |
| Prerequisites | None — a fundamentals exam for technical and non-technical audiences |

## Domain weights

| Domain | Weight | Chapters |
|---|---|---|
| 1.0 Describe cloud concepts | 25–30% | 3 |
| 2.0 Describe Azure architecture and services | **35–40%** | 4 |
| 3.0 Describe Azure management and governance | 30–35% | 4 |

Architecture & services is the biggest domain, but management & governance is
barely behind it — the two Azure-specific domains together are ~70% of the
exam. Cloud concepts is smaller but the easiest place to bank points, since it
is pure vocabulary (shared responsibility, cloud models, IaaS/PaaS/SaaS).

## Chapters

### Domain 1 — Describe Cloud Concepts (25–30%)
- [1.1 Cloud Computing](domain-1-cloud-concepts/1.1-cloud-computing.md)
- [1.2 Benefits of Cloud Services](domain-1-cloud-concepts/1.2-cloud-benefits.md)
- [1.3 Cloud Service Types (IaaS, PaaS, SaaS)](domain-1-cloud-concepts/1.3-cloud-service-types.md)

### Domain 2 — Describe Azure Architecture & Services (35–40%)
- [2.1 Core Architectural Components](domain-2-azure-architecture-services/2.1-core-architectural-components.md)
- [2.2 Compute & Networking Services](domain-2-azure-architecture-services/2.2-compute-networking.md)
- [2.3 Storage Services](domain-2-azure-architecture-services/2.3-storage.md)
- [2.4 Identity, Access & Security](domain-2-azure-architecture-services/2.4-identity-access-security.md)

### Domain 3 — Describe Azure Management & Governance (30–35%)
- [3.1 Cost Management](domain-3-management-governance/3.1-cost-management.md)
- [3.2 Governance & Compliance](domain-3-management-governance/3.2-governance-compliance.md)
- [3.3 Managing & Deploying Resources](domain-3-management-governance/3.3-managing-deploying-resources.md)
- [3.4 Monitoring Tools](domain-3-management-governance/3.4-monitoring-tools.md)

### Reference
- [Acronym List](acronyms.md) — every acronym and short name worth knowing for AZ-900

## The study games

A terminal study-game suite lives in `../study-games/`. Launch it with:

```bash
cd ../study-games
python3 az900.py
```

Every chapter here has a matching game topic with quizzes, flashcards, and
term-matching. There are also global modes:

- **Exam simulator** — 45 questions weighted exactly like the real exam, timed
- **Azure gym** — infinitely generated problems, 3 levels: shared
  responsibility, scope & hierarchy, redundancy & SLA math
- **Service blitz** — 50 core Azure services, name-from-description and
  category questions, with streaks
- **Acronym blitz** — the AZ-900 acronym list, fuzzy-graded
- **Review missed** — every question you've ever gotten wrong, until you clear it
- **Stats** — accuracy per topic and your three weakest areas

Progress persists between sessions in `study-games/.progress.json`.

## Suggested study plan

1. **Read one chapter, then play its topic games immediately.** Retrieval right
   after reading is what makes it stick.
2. **Hit the Azure gym daily.** The shared responsibility model and the
   management-group → subscription → resource-group hierarchy show up all over
   the exam in scenario form — they should become reflexes.
3. **Run Service blitz and Acronym blitz as warm-ups** at the start of each
   session. Most AZ-900 questions reduce to "which service does X?" — the blitz
   trains exactly that mapping.
4. **Clear your review pile weekly** (R in the main menu). A question isn't
   "done" until you've answered it correctly after missing it.
5. **Take the exam simulator when topic accuracy is ≥80% across the board.**
   Score 80%+ on two consecutive simulations before booking the real exam.
6. Exam-day mechanics: AZ-900 has no penalty for guessing — never leave a
   blank. Watch for "which TWO..." questions, and read scenario questions for
   the one keyword (e.g., "without managing the operating system") that maps to
   a service model or service.
