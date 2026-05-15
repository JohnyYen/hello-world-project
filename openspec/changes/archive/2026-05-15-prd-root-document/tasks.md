# Tasks: Root-Level Product Requirements Document (PRD.md)

## Phase 1: Research & Sourcing

- [x] 1.1 Read `PRD_example.md` at project root to understand the structural template and adapt it for an educational platform
- [x] 1.2 Read `apps/backend/docs/user_stories.md` to source feature catalog, role definitions, workflows, and identify what to reference vs. extract
- [x] 1.3 Read `apps/backend/README.md`, `apps/frontend/README.md`, and `apps/game/README.md` to understand component architecture, tech stacks, and cross-cutting concerns
- [x] 1.4 Read `apps/game/LEVEL_1_DEVELOPMENT_ROADMAP.md` to source game-specific roadmap items for the Release Roadmap section
- [x] 1.5 Read `apps/backend/docs/database-design.md` to understand data model for architecture and integration sections
- [x] 1.6 Read `AGENTS.md` at project root to capture cross-project conventions, user roles, and testing strategy
- [x] 1.7 Research competitive landscape: visit Scratch, Code.org, and Tynker to gather comparison data for Section 12 (Competitive Landscape)
- [x] 1.8 Research xAPI 1.0 specification and LMS APIs (Moodle LTI 1.3, Canvas API) for Section 8 (Integration Points)
- [x] 1.9 Compile a research brief summarizing key findings, source mappings (which section draws from which doc), and content gaps requiring new writing

## Phase 2: Draft Sections 1–4

- [x] 2.1 Write Section 1 (Problem Statement): Define the educational gap, limitations of existing approaches, rationale for visual programming + adaptive learning, and supporting research citations (REQ-PS-01 through REQ-PS-04)
- [x] 2.2 Write Section 2 (Vision & Mission): Draft vision statement (1-3 sentences), mission statement, educational philosophy (constructivism/project-based/mastery learning), and 3-5 core values (REQ-VM-01 through REQ-VM-04)
- [x] 2.3 Write Section 3 (Target Users): Define K-12 student persona, university student persona, professor persona, administrator persona, and institutional buyer persona (optional) with goals, pain points, and context (REQ-TU-01 through REQ-TU-04)
- [x] 2.4 Write Section 4 (User Roles & Permissions): Define Admin/Professor/Student roles, create permission matrix table, document role hierarchy, and cite sources from user_stories.md (REQ-UR-01 through REQ-UR-04)

## Phase 3: Draft Sections 5–8

- [x] 3.1 Write Section 5 (Feature Catalog): Group features by component (Game/Frontend/Backend), assign P0/P1/P2 priorities with justification, write 1-3 sentence descriptions per feature, note cross-component dependencies, and identify at least 3 future planned features (REQ-FC-01 through REQ-FC-05)
- [x] 3.2 Write Section 6 (User Workflows): Document at least 4 end-to-end flows (course creation, gameplay, progress sync, analytics), include one Mermaid sequence/flowchart diagram, and describe error/edge case paths including offline gameplay (REQ-UW-01 through REQ-UW-03)
- [x] 3.3 Write Section 7 (Technical Architecture): Create high-level Mermaid component interaction diagram, describe API contract pattern (OpenAPI at `packages/api-contract/`), outline monorepo structure, describe offline sync architecture, and reference existing architecture docs (REQ-TA-01 through REQ-TA-05)
- [x] 3.4 Write Section 8 (Integration Points): Describe xAPI 1.0 integration with statement types, document Moodle and Canvas LMS integration requirements, describe offline sync protocol with queue and conflict resolution, and assign priority/phasing per integration (REQ-IP-01 through REQ-IP-04)

## Phase 4: Draft Sections 9–13

- [x] 4.1 Write Section 9 (Non-Functional Requirements): Specify quantified performance targets (API p95/p99, game load time, concurrency), security model (JWT, RBAC, encryption, PII), Spanish-first i18n strategy with framework choice, accessibility targets (WCAG 2.1 Level AA) for web and game, and scalability milestones (MVP/12mo/24mo) (REQ-NF-01 through REQ-NF-05)
- [x] 4.2 Write Section 10 (Success Metrics & KPIs): Define at least 3 student-level KPIs, 2 professor/admin adoption KPIs, learning outcome measurement approach, and 2 business KPIs — each with data source, calculation method, and review cadence (REQ-SM-01 through REQ-SM-04)
- [x] 4.3 Write Section 11 (Release Roadmap): Define at least 3 phases with entry/exit criteria, show dependency chain between phases, describe versioning strategy (semver), and specify component release model (independent vs. coordinated) (REQ-RR-01 through REQ-RR-04)
- [x] 4.4 Write Section 12 (Competitive Landscape): Compare against Scratch, Code.org, and Tynker across at least 5 dimensions, write differentiation statement per competitor, define market position, and include feature comparison matrix table (REQ-CL-01 through REQ-CL-04)
- [x] 4.5 Write Section 13 (Open Questions): Catalog at least 8 open questions spanning architecture, product, process, and integration dimensions — each with context, options, and decision-maker; include at least 1 resolved question with date/decision/rationale (REQ-OQ-01 through REQ-OQ-04)

## Phase 5: Polish & Review

- [x] 5.1 Add front matter: version (`0.1.0-draft`), author, status (`Draft`), and last-updated date to the PRD header (CC-2)
- [x] 5.2 Verify all sections use RFC 2119 keywords (MUST/SHOULD/MAY) consistently for requirements and constraints (CC-3)
- [x] 5.3 Verify all P0/P1/P2 priority labels are consistent and every P0 feature has a justification (CC-4)
- [x] 5.4 Verify every Mermaid diagram has a descriptive preceding paragraph explaining what it shows (CC-5)
- [x] 5.5 Check tone and style: ensure professional, clear language suitable for both technical and non-technical readers; remove any marketing language (CC-6)
- [x] 5.6 Verify section independence: check each of the 13 sections can be read standalone without unexplained acronyms or project-specific terms (CC-7)
- [x] 5.7 Validate all cross-references: ensure all relative paths from project root point to existing files and link to specific sections where possible (CC-8)
- [x] 5.8 Check document length: verify total is between 5,000–15,000 words and no single section exceeds 30% of the total (CC-9)
- [x] 5.9 Verify all Mermaid diagrams render as valid GFM and all tables have aligned columns (CC-1)
- [x] 5.10 Run a final consistency pass: confirm no contradictions between sections, no orphaned references, and all acceptance criteria from Sections 1-13 are covered

## Phase 6: README Update

- [x] 6.1 Add a link to `PRD.md` in the root `README.md` documentation overview section with descriptive label (e.g., "Product Requirements Document") — limit changes to this addition only (REQ-README-01, REQ-README-02)

## Phase 7: Verification

- [x] 7.1 Verify Section 1 acceptance criteria: problem stateable in one sentence, 2+ pain points per role, visual programming + adaptive learning rationale, research citations present or noted as open questions
- [x] 7.2 Verify Section 2 acceptance criteria: vision 1-3 sentences, mission differentiates, philosophy named, 3-5 core values, reader can explain "why"
- [x] 7.3 Verify Section 3 acceptance criteria: 3+ personas defined, student has K-12 and university sub-personas, persona has goals/pain points/context, institution persona exists or noted
- [x] 7.4 Verify Section 4 acceptance criteria: roles defined, permission matrix exists, hierarchy documented, source references included, no role contradicts Section 9 security
- [x] 7.5 Verify Section 5 acceptance criteria: features grouped by component, P0/P1/P2 labels with justification, descriptions 1-3 sentences, cross-component deps noted, all existing features cataloged, 3+ future features
- [x] 7.6 Verify Section 6 acceptance criteria: 4+ workflows, Mermaid diagram included, happy path + error path per workflow, traceable to Section 5 features, offline sync addressed
- [x] 7.7 Verify Section 7 acceptance criteria: Mermaid architecture diagram, API contract pattern described, monorepo outlined, offline sync described, existing docs referenced
- [x] 7.8 Verify Section 8 acceptance criteria: xAPI described with statement types, Moodle integration documented, Canvas integration documented or noted future, offline sync with queue/conflict resolution, priority per integration
- [x] 7.9 Verify Section 9 acceptance criteria: quantified performance targets, security model covers auth/RBAC/encryption/PII, Spanish-first i18n, WCAG level specified, scalability with 3 milestones
- [x] 7.10 Verify Section 10 acceptance criteria: 3+ student KPIs with calculation, 2+ adoption KPIs, learning outcome approach defined, 2+ business KPIs, each KPI has data source and cadence
- [x] 7.11 Verify Section 11 acceptance criteria: 3+ phases with entry/exit criteria, dependency chain documented, versioning strategy defined, component release model described, features mapped to phases
- [x] 7.12 Verify Section 12 acceptance criteria: 3+ competitors, 5+ comparison dimensions, differentiation per competitor, market position defined (or TBD), feature comparison matrix included (or noted)
- [x] 7.13 Verify Section 13 acceptance criteria: 8+ open questions across 4 dimensions, each with context/options/decision-maker, 1+ resolved question, questions categorized, questions actionable
- [x] 7.14 Verify README acceptance criteria: link to PRD.md exists, no unrelated changes, link in documentation section with clear label
- [x] 7.15 Cross-verify all CC requirements (CC-1 through CC-9) are met across the entire document
