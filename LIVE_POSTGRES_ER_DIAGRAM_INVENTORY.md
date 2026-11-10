# Live PostgreSQL ER Diagram Inventory

Generated directly from the configured PostgreSQL database.

## Tables
### `cmb_item_concepts`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `item_id` | `INTEGER` | NOT NULL | PK + FK |
| `concept_id` | `INTEGER` | NOT NULL | PK + FK |

Foreign keys:
- `concept_id` → `concepts` (`concept_id`)
- `item_id` → `cmb_items` (`item_id`)

### `concept_prerequisites`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `concept_id` | `INTEGER` | NOT NULL | PK + FK |
| `prerequisite_concept_id` | `INTEGER` | NOT NULL | PK + FK |

Foreign keys:
- `concept_id` → `concepts` (`concept_id`)
- `prerequisite_concept_id` → `concepts` (`concept_id`)

### `material_sections`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `section_id` | `INTEGER` | NOT NULL | PK |
| `material_id` | `INTEGER` | NOT NULL | FK + UQ |
| `section_order` | `INTEGER` | NOT NULL | UQ |
| `text` | `TEXT` | NOT NULL | — |
| `source_location_type` | `VARCHAR(50)` | NOT NULL | — |
| `source_location_value` | `VARCHAR(100)` | NOT NULL | — |

Foreign keys:
- `material_id` → `materials` (`material_id`)

### `submissions`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `submission_id` | `INTEGER` | NOT NULL | PK |
| `assignment_id` | `INTEGER` | NOT NULL | FK + UQ |
| `user_id` | `INTEGER` | NOT NULL | FK + UQ |
| `submitted_at` | `TIMESTAMP` | NOT NULL | — |
| `work_reference` | `VARCHAR(512)` | NOT NULL | — |
| `marking_status` | `VARCHAR(50)` | NOT NULL | — |

Foreign keys:
- `assignment_id` → `assignments` (`assignment_id`)
- `user_id` → `users` (`user_id`)

### `ai_gateway_request_sources`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `request_id` | `INTEGER` | NOT NULL | PK + FK |
| `section_id` | `INTEGER` | NOT NULL | PK + FK |

Foreign keys:
- `request_id` → `ai_gateway_requests` (`request_id`)
- `section_id` → `material_sections` (`section_id`)

### `diagnostic_sessions`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `session_id` | `INTEGER` | NOT NULL | PK |
| `submission_id` | `INTEGER` | NOT NULL | FK |
| `started_at` | `TIMESTAMP` | NOT NULL | — |
| `completed_at` | `TIMESTAMP` | NULL | — |

Foreign keys:
- `submission_id` → `submissions` (`submission_id`)

### `roles`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `role_id` | `INTEGER` | NOT NULL | PK |
| `name` | `VARCHAR(50)` | NOT NULL | — |

### `users`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `user_id` | `INTEGER` | NOT NULL | PK |
| `username` | `VARCHAR(50)` | NULL | — |
| `email` | `VARCHAR(255)` | NOT NULL | — |
| `password_hash` | `VARCHAR(255)` | NOT NULL | — |
| `account_status` | `VARCHAR(50)` | NOT NULL | — |
| `created_at` | `TIMESTAMP` | NOT NULL | — |
| `department_id` | `INTEGER` | NULL | FK |

Foreign keys:
- `department_id` → `departments` (`department_id`)

### `access_logs`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `log_id` | `INTEGER` | NOT NULL | PK |
| `user_id` | `INTEGER` | NULL | FK |
| `action` | `VARCHAR(100)` | NOT NULL | — |
| `target_type` | `VARCHAR(100)` | NOT NULL | — |
| `target_id` | `VARCHAR(100)` | NOT NULL | — |
| `occurred_at` | `TIMESTAMP` | NOT NULL | — |

Foreign keys:
- `user_id` → `users` (`user_id`)

### `courses`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `course_id` | `INTEGER` | NOT NULL | PK |
| `title` | `VARCHAR(255)` | NOT NULL | — |
| `owner_user_id` | `INTEGER` | NOT NULL | FK |
| `ai_enabled` | `BOOLEAN` | NOT NULL | — |
| `department_id` | `INTEGER` | NOT NULL | FK |

Foreign keys:
- `owner_user_id` → `users` (`user_id`)
- `department_id` → `departments` (`department_id`)

### `lecturer_approval_events`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `approval_id` | `INTEGER` | NOT NULL | PK |
| `lecturer_user_id` | `INTEGER` | NOT NULL | FK |
| `administrator_user_id` | `INTEGER` | NOT NULL | FK |
| `decision` | `VARCHAR(50)` | NOT NULL | — |
| `decided_at` | `TIMESTAMP` | NOT NULL | — |

Foreign keys:
- `administrator_user_id` → `users` (`user_id`)
- `lecturer_user_id` → `users` (`user_id`)

### `user_roles`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `user_id` | `INTEGER` | NOT NULL | PK + FK |
| `role_id` | `INTEGER` | NOT NULL | PK + FK |
| `assigned_at` | `TIMESTAMP` | NOT NULL | — |
| `assigned_by` | `INTEGER` | NULL | FK |

Foreign keys:
- `assigned_by` → `users` (`user_id`)
- `role_id` → `roles` (`role_id`)
- `user_id` → `users` (`user_id`)

### `ai_gateway_requests`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `request_id` | `INTEGER` | NOT NULL | PK |
| `user_id` | `INTEGER` | NOT NULL | FK |
| `course_id` | `INTEGER` | NOT NULL | FK |
| `purpose` | `VARCHAR(100)` | NOT NULL | — |
| `provider` | `VARCHAR(100)` | NOT NULL | — |
| `status` | `VARCHAR(50)` | NOT NULL | — |
| `created_at` | `TIMESTAMP` | NOT NULL | — |

Foreign keys:
- `course_id` → `courses` (`course_id`)
- `user_id` → `users` (`user_id`)

### `assignments`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `assignment_id` | `INTEGER` | NOT NULL | PK |
| `course_id` | `INTEGER` | NOT NULL | FK |
| `title` | `VARCHAR(255)` | NOT NULL | — |
| `due_at` | `TIMESTAMP` | NOT NULL | — |
| `lifecycle_status` | `VARCHAR(50)` | NOT NULL | — |
| `results_released_at` | `TIMESTAMP` | NULL | — |
| `results_released_by` | `INTEGER` | NULL | FK |
| `cmb_enabled` | `BOOLEAN` | NOT NULL | — |

Foreign keys:
- `course_id` → `courses` (`course_id`)
- `results_released_by` → `users` (`user_id`)

### `cmb_items`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `item_id` | `INTEGER` | NOT NULL | PK |
| `course_id` | `INTEGER` | NOT NULL | FK |
| `item_type` | `VARCHAR(50)` | NOT NULL | — |
| `prompt` | `TEXT` | NOT NULL | — |
| `review_status` | `VARCHAR(50)` | NOT NULL | — |
| `approved_by` | `INTEGER` | NULL | FK |

Foreign keys:
- `approved_by` → `users` (`user_id`)
- `course_id` → `courses` (`course_id`)

### `concepts`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `concept_id` | `INTEGER` | NOT NULL | PK |
| `course_id` | `INTEGER` | NOT NULL | FK + UQ |
| `name` | `VARCHAR(255)` | NOT NULL | UQ |

Foreign keys:
- `course_id` → `courses` (`course_id`)

### `enrolments`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `course_id` | `INTEGER` | NOT NULL | PK + FK |
| `user_id` | `INTEGER` | NOT NULL | PK + FK |
| `status` | `VARCHAR(50)` | NOT NULL | — |
| `enrolled_at` | `TIMESTAMP` | NOT NULL | — |

Foreign keys:
- `course_id` → `courses` (`course_id`)
- `user_id` → `users` (`user_id`)

### `materials`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `material_id` | `INTEGER` | NOT NULL | PK |
| `course_id` | `INTEGER` | NOT NULL | FK |
| `uploaded_by` | `INTEGER` | NOT NULL | FK |
| `file_path` | `VARCHAR(512)` | NOT NULL | — |
| `processing_status` | `VARCHAR(50)` | NOT NULL | — |
| `uploaded_at` | `TIMESTAMP` | NOT NULL | — |

Foreign keys:
- `course_id` → `courses` (`course_id`)
- `uploaded_by` → `users` (`user_id`)

### `assignment_questions`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `question_id` | `INTEGER` | NOT NULL | PK |
| `assignment_id` | `INTEGER` | NOT NULL | FK + UQ |
| `prompt` | `TEXT` | NOT NULL | — |
| `max_score` | `NUMERIC(5, 2)` | NOT NULL | — |
| `position` | `INTEGER` | NOT NULL | UQ |

Foreign keys:
- `assignment_id` → `assignments` (`assignment_id`)

### `marks`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `submission_id` | `INTEGER` | NOT NULL | PK + FK |
| `question_id` | `INTEGER` | NOT NULL | PK + FK |
| `score` | `NUMERIC(5, 2)` | NOT NULL | — |
| `lecturer_comment` | `TEXT` | NULL | — |
| `graded_by` | `INTEGER` | NOT NULL | FK |
| `graded_at` | `TIMESTAMP` | NOT NULL | — |

Foreign keys:
- `graded_by` → `users` (`user_id`)
- `question_id` → `assignment_questions` (`question_id`)
- `submission_id` → `submissions` (`submission_id`)

### `material_section_concepts`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `section_id` | `INTEGER` | NOT NULL | PK + FK |
| `concept_id` | `INTEGER` | NOT NULL | PK + FK |

Foreign keys:
- `concept_id` → `concepts` (`concept_id`)
- `section_id` → `material_sections` (`section_id`)

### `question_concepts`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `question_id` | `INTEGER` | NOT NULL | PK + FK |
| `concept_id` | `INTEGER` | NOT NULL | PK + FK |

Foreign keys:
- `concept_id` → `concepts` (`concept_id`)
- `question_id` → `assignment_questions` (`question_id`)

### `candidate_explanations`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `explanation_id` | `INTEGER` | NOT NULL | PK |
| `session_id` | `INTEGER` | NOT NULL | FK |
| `concept_id` | `INTEGER` | NOT NULL | FK |
| `label` | `VARCHAR(255)` | NOT NULL | — |
| `confidence` | `DOUBLE PRECISION` | NOT NULL | — |

Foreign keys:
- `concept_id` → `concepts` (`concept_id`)
- `session_id` → `diagnostic_sessions` (`session_id`)

### `responses`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `response_id` | `INTEGER` | NOT NULL | PK |
| `session_id` | `INTEGER` | NOT NULL | FK |
| `item_id` | `INTEGER` | NOT NULL | FK |
| `answer` | `TEXT` | NOT NULL | — |
| `confidence_choice` | `VARCHAR(50)` | NULL | — |
| `response_time` | `INTEGER` | NULL | — |

Foreign keys:
- `item_id` → `cmb_items` (`item_id`)
- `session_id` → `diagnostic_sessions` (`session_id`)

### `interventions`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `intervention_id` | `INTEGER` | NOT NULL | PK |
| `explanation_id` | `INTEGER` | NOT NULL | FK |

Foreign keys:
- `explanation_id` → `candidate_explanations` (`explanation_id`)

### `followup_results`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `followup_id` | `INTEGER` | NOT NULL | PK |
| `intervention_id` | `INTEGER` | NOT NULL | FK |
| `item_id` | `INTEGER` | NOT NULL | FK |
| `correct` | `BOOLEAN` | NOT NULL | — |
| `answered_at` | `TIMESTAMP` | NOT NULL | — |

Foreign keys:
- `intervention_id` → `interventions` (`intervention_id`)
- `item_id` → `cmb_items` (`item_id`)

### `recommended_resources`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `intervention_id` | `INTEGER` | NOT NULL | PK + FK |
| `section_id` | `INTEGER` | NOT NULL | PK + FK |
| `reason` | `TEXT` | NULL | — |

Foreign keys:
- `intervention_id` → `interventions` (`intervention_id`)
- `section_id` → `material_sections` (`section_id`)

### `faculties`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `faculty_id` | `INTEGER` | NOT NULL | PK |
| `name` | `VARCHAR(255)` | NOT NULL | UQ |
| `code` | `VARCHAR(50)` | NOT NULL | UQ |

### `departments`

| Column | PostgreSQL type | Null | Key |
|---|---|---:|---|
| `department_id` | `INTEGER` | NOT NULL | PK |
| `faculty_id` | `INTEGER` | NOT NULL | FK + UQ |
| `name` | `VARCHAR(255)` | NOT NULL | UQ |
| `code` | `VARCHAR(50)` | NOT NULL | UQ |

Foreign keys:
- `faculty_id` → `faculties` (`faculty_id`)
