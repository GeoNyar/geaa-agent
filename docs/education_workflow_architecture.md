# Education Workflow System: Architecture and MVP Plan

## 1. Purpose

The Education Workflow System is a planned GEAA capability that helps educators organise course delivery, develop teaching and assessment resources, analyse learner progress, and maintain evidence of learning. It should support both school and TVET contexts while remaining grounded in the curriculum, course outline, or occupational standard supplied by the educator.

This document defines the initial design. It does not claim that these capabilities have already been implemented.

## 2. Design principles

1. **Source-grounded:** use the uploaded or selected curriculum, course outline, learning outcomes, or occupational standard as the primary reference. Do not invent official requirements.
2. **Educator-controlled:** generated materials are drafts. The educator reviews, edits, and approves them before classroom use or sharing.
3. **Traceable:** distinguish supplied source information, uploaded data, generated suggestions, calculations, and items requiring verification.
4. **Modular:** add the workflow as a separate feature area; avoid destabilising GEAA's existing assistant, retrieval, research, analytics, and presentation features.
5. **Privacy-conscious:** use fictional data in public demonstrations and tests. Do not expose identifiable learner records, marks, or attendance data in public outputs.
6. **Incremental:** implement and test one complete workflow slice before adding further modules.

## 3. Proposed workflow

`Course context → Outcomes → Teaching plan → Learning resources → Assessment → Marking → Learner progress → Portfolio evidence`

Each stage should retain its relationship to the course context and relevant learning outcomes.

## 4. Proposed modules

| Module | Main responsibility | Example outputs |
|---|---|---|
| Course setup | Capture course/unit, level, duration, learner group, delivery context, and source documents | Course profile and source register |
| Outcomes | Extract or map outcomes from the supplied source | Outcome register and outcome-to-content map |
| Teaching plan | Organise content and outcomes across available teaching time | Scheme of work, lesson plan, lesson notes |
| Resource studio | Prepare resources aligned to the selected lesson and outcomes | Slides, worksheets, practical activities, observation checklists |
| Assessment studio | Design assessment tasks and criteria | CATs, quizzes, tutorials, practical and summative assessments, marking guides or rubrics |
| Marks and attendance | Record educator-entered learner results and attendance | Mark sheet, attendance register, class summary |
| Progress and portfolio | Summarise evidence against outcomes | Outcome-level progress summary and portfolio record |

The modules are a target design, not a statement that every output is currently available.

## 5. First MVP: one end-to-end course workflow

Build the smallest useful vertical slice in this order:

1. Create a course profile using educator-entered details and one supplied course source.
2. Capture or map a small set of learning outcomes, preserving the source wording and references.
3. Generate one lesson plan linked to selected outcomes.
4. Generate one assessment and a corresponding marking guide.
5. Enter a small set of fictional learner marks and calculate transparent summaries.
6. Produce a draft course evidence summary showing which outcomes were addressed and what evidence is available.

**MVP boundary:** start with one course/unit and a small number of outcomes. Do not attempt automated social-media responses, full institutional records, multi-course scheduling, or complex analytics in the first release.

## 6. Data and evidence model

The initial design should keep these records conceptually separate:

- **Course:** course or unit identity, level, duration, delivery context, and source references.
- **Source:** document name, source type, version/date if known, and relevant page/section.
- **Outcome:** source wording, reference, and any educator-approved interpretation.
- **Teaching activity:** date or teaching week, content, selected outcomes, and resource links.
- **Assessment:** task, assessment type, maximum score, criteria, and linked outcomes.
- **Learner result:** learner identifier, assessment, score, and educator-entered status.
- **Attendance:** session, learner identifier, and attendance status.
- **Evidence item:** resource or assessment record, linked outcomes, review status, and date.

For early demonstrations, learner identifiers and results must be fictional. Any future real-learner data feature requires an explicit data-protection and access-control design before deployment.

## 7. Output status and provenance

Every generated or analysed item should make its status clear:

- **SOURCE-PROVIDED:** directly supplied in a curriculum, course outline, standard, or uploaded file.
- **EDUCATOR-ENTERED:** information entered or confirmed by the educator.
- **GENERATED-DRAFT:** AI-generated content that has not yet been approved.
- **CALCULATED:** results produced from entered data using stated rules.
- **NEEDS-VERIFICATION:** information that cannot be confirmed from the available source.

Do not present generated material as an official curriculum requirement. Do not treat synthetic demonstration results as evidence about real learners or institutions.

## 8. Technical approach

- Keep the existing GEAA application and working features intact.
- Develop the workflow in a separate feature area, with small modules that can later be connected to the Streamlit interface.
- Reuse GEAA's existing Gemini integration and retrieval capabilities where appropriate; do not introduce a second AI provider or require an OpenAI API.
- Keep business logic separate from interface code so that calculations and validation can be tested independently.
- Begin with clearly labelled session-level or downloadable draft outputs. Do not promise permanent storage until persistence, backup, access control, and data-retention behaviour have been implemented and tested.
- Add automated tests using synthetic course and learner data.

## 9. Quality checks before release

- Each lesson and assessment can be traced to one or more selected outcomes.
- Source wording is not silently altered or presented as an official requirement when it is generated.
- Assessment totals, mark calculations, and summaries are reproducible and tested.
- Missing or ambiguous source information is flagged rather than guessed.
- Draft status and educator review requirements are visible.
- Public tests and examples contain no real learner personal data.
- Existing GEAA tests and workflows continue to pass.

## 10. Delivery sequence

| Phase | Deliverable | Exit condition |
|---|---|---|
| 0. Architecture | This scope, workflow, and data design | Scope reviewed before implementation |
| 1. Course and outcomes | Course profile and outcome register | Source and outcome links are traceable |
| 2. Lesson planning | One outcome-linked lesson plan | Draft can be reviewed and edited |
| 3. Assessment | Assessment and marking guide | Tasks and criteria map to outcomes |
| 4. Marks and progress | Fictional mark entry and transparent summaries | Calculations pass tests |
| 5. Portfolio | Draft evidence summary | Evidence links back to course outcomes |
| 6. Expansion | Additional resources, attendance, TVET standards, persistence, and reporting | Each addition has privacy, validation, and regression checks |

## 11. Current status

**Status: design only.** This document establishes the proposed architecture and MVP boundary on the `feature/education-workflow-prototype` branch. No existing GEAA application code is changed by this document.
