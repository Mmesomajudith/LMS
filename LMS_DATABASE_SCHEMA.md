# LMS Database Schema and Normalization Decisions

This is a standalone logical database design based on `LMS DOC..docx`. It is not tied to a repository, framework, or database engine.

`PK` means primary key; `FK` means foreign key. `UNIQUE` and `CHECK` indicate constraints.

## Identity and Access

- **users**: `user_id` PK, `email` UNIQUE, `password_hash`, `account_status`, `created_at`
- **roles**: `role_id` PK, `name` UNIQUE. Values include `student`, `lecturer`, and `administrator`.
- **user_roles**: `user_id` FK, `role_id` FK, `assigned_at`, `assigned_by` FK to `users`; composite PK (`user_id`, `role_id`)
- **lecturer_approval_events**: `approval_id` PK, `lecturer_user_id` FK to `users`, `administrator_user_id` FK to `users`, `decision`, `decided_at`

Approval events are separate from user identity and role assignment so approval history can be retained without duplicating user attributes.

## Courses and Materials

- **courses**: `course_id` PK, `title`, `owner_user_id` FK to `users`, `ai_enabled`
- **enrolments**: `course_id` FK, `user_id` FK, `status`, `enrolled_at`; composite PK (`course_id`, `user_id`)
- **concepts**: `concept_id` PK, `course_id` FK, `name`; UNIQUE (`course_id`, `name`)
- **concept_prerequisites**: `concept_id` FK, `prerequisite_concept_id` FK to `concepts`; composite PK (`concept_id`, `prerequisite_concept_id`)
- **materials**: `material_id` PK, `course_id` FK, `uploaded_by` FK to `users`, `file_path`, `processing_status`, `uploaded_at`
- **material_sections**: `section_id` PK, `material_id` FK, `section_order`, `text`, `source_location_type`, `source_location_value`; UNIQUE (`material_id`, `section_order`)
- **material_section_concepts**: `section_id` FK, `concept_id` FK; composite PK (`section_id`, `concept_id`)

## Assessment

- **assignments**: `assignment_id` PK, `course_id` FK, `title`, `due_at`, `lifecycle_status`, `results_released_at`, `results_released_by` FK to `users`, `cmb_enabled`
- **assignment_questions**: `question_id` PK, `assignment_id` FK, `prompt`, `max_score`, `position`
- **question_concepts**: `question_id` FK, `concept_id` FK; composite PK (`question_id`, `concept_id`)
- **submissions**: `submission_id` PK, `assignment_id` FK, `user_id` FK, `submitted_at`, `work_reference`, `marking_status`
- **marks**: `submission_id` FK, `question_id` FK, `score`, `lecturer_comment`, `graded_by` FK to `users`, `graded_at`; composite PK (`submission_id`, `question_id`)

## Concept-to-Mastery Bridge (CMB)

- **cmb_items**: `item_id` PK, `course_id` FK, `item_type` (`diagnostic`, `practice`, or `verification`), `prompt`, `review_status`, `approved_by` FK to `users`
- **cmb_item_concepts**: `item_id` FK, `concept_id` FK; composite PK (`item_id`, `concept_id`)
- **diagnostic_sessions**: `session_id` PK, `submission_id` FK, `started_at`, `completed_at`
- **responses**: `response_id` PK, `session_id` FK, `item_id` FK to `cmb_items`, `answer`, `confidence_choice`, `response_time`
- **candidate_explanations**: `explanation_id` PK, `session_id` FK, `concept_id` FK, `label`, `confidence`
- **interventions**: `intervention_id` PK, `explanation_id` FK
- **recommended_resources**: `intervention_id` FK, `section_id` FK to `material_sections`, `reason`; composite PK (`intervention_id`, `section_id`)
- **followup_results**: `followup_id` PK, `intervention_id` FK, `item_id` FK to `cmb_items`, `correct`, `answered_at`

A follow-up must use a verification item, not the original assessment item. A response must use an item of a permitted diagnostic or practice type, according to the CMB workflow.

## Audit and AI Gateway

- **access_logs**: `log_id` PK, `user_id` FK, `action`, `target_type`, `target_id`, `occurred_at`
- **ai_gateway_requests**: `request_id` PK, `user_id` FK, `course_id` FK, `purpose`, `provider`, `status`, `created_at`
- **ai_gateway_request_sources**: `request_id` FK, `section_id` FK to `material_sections`; composite PK (`request_id`, `section_id`)

`access_logs.target_type` and `target_id` form a polymorphic reference, so normal foreign-key enforcement is not available for every target type. Keep it audit-focused and enforce authorization in application logic. The AI Gateway log should record source references and request metadata; avoid retaining sensitive prompt content unless retention is explicitly required.

## Relationships

- Users and Roles are many-to-many through `user_roles`.
- A lecturer owns Courses. Users and Courses are many-to-many through `enrolments`.
- Courses have Concepts, Materials, and Assignments.
- Concepts can depend on other Concepts through `concept_prerequisites`.
- Materials have Material Sections; sections map to Concepts through `material_section_concepts`.
- Assignments have Assignment Questions; questions map to Concepts through `question_concepts`.
- Each Submission belongs to one Assignment and one User. Marks belong to a Submission and an Assignment Question.
- A Submission can have Diagnostic Sessions. Sessions contain Responses and Candidate Explanations.
- Candidate Explanations can lead to Interventions. Interventions link to recommended material sections and follow-up results.
- CMB items are mapped to Concepts and are referenced by diagnostic Responses and Follow-up Results.
- Users generate Access Logs. AI Gateway requests can reference the lecturer-approved source sections used.

## Normalization Decisions

### First Normal Form (1NF)

- Store one value per field; do not store comma-separated roles, concepts, prerequisites, resources, or answers.
- Represent repeating relationships as separate rows in junction tables.
- Keep each assessment response, mark, recommendation, and prerequisite link as its own record.

### Second Normal Form (2NF)

- In tables with composite keys, every non-key attribute depends on the complete key.
- For example, a recommendation `reason` depends on the specific (`intervention_id`, `section_id`) pair.
- An enrolment's status depends on the (`course_id`, `user_id`) pair, not just one side.

### Third Normal Form (3NF)

- Store each entity's descriptive attributes only in its own table: role names in `roles`, course titles in `courses`, concept names in `concepts`, and section text in `material_sections`.
- Store references as foreign keys instead of copying names or titles into enrolments, submissions, marks, and recommendations.
- Keep question score limits with the assignment-question relationship, not on reusable CMB items.

## Integrity and Derived Data

- Calculate grade totals, class analytics, and CMB eligibility from source records rather than persisting duplicated aggregates.
- Use `results_released_at` rather than storing both a release timestamp and a redundant released flag; a null timestamp means unreleased.
- Keep workflow states such as `account_status`, `processing_status`, `lifecycle_status`, and `marking_status` only where explicit transitions are needed.
- Enforce that a submission's marked question belongs to its assignment, and that mapped materials, questions, and CMB items refer to concepts in the same course.
- Prevent a concept from being its own prerequisite and reject prerequisite cycles.
- Suppress lecturer analytics for groups below the minimum size specified by the project documentation.
- The reading companion is ungraded and must not read marks or create diagnostic records unless the student opts in.

## Assumptions to Confirm

- This design treats result release as assignment-wide, following the document's assignment-level release fields. If release is per student, move release timestamp and releaser to `submissions`.
- `assignment_questions` models assignment-specific questions. If questions must be reused across assignments, split question content into a reusable `question_items` table and connect it through an `assignment_questions` junction/association table.
- The document does not specify exact status values, database types, retention periods, or the minimum analytics group size; decide these during implementation.
