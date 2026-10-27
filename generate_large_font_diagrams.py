"""Generate diagrams with large, highly legible fonts optimized for Word document embedding.

Includes:
1. Master Conceptual / Logical ER Diagram (er_diagram.png) with large fonts.
2. Complete Physical Schema Blueprint (complete_schema_diagram.png).
3. Five dedicated Domain-Specific Schema Diagrams with large (10-14pt) fonts:
   - schema_d1_identity.png
   - schema_d2_courses.png
   - schema_d3_assessment.png
   - schema_d4_cmb.png
   - schema_d5_audit.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


# ----------------------------------------------------------------------
# 1. DOMAIN-SPECIFIC SCHEMA DIAGRAMS (LARGE, CRYSTAL-CLEAR FONTS)
# ----------------------------------------------------------------------

def generate_domain_diagram(
    filename,
    title,
    subtitle,
    header_color,
    border_color,
    tables,
    connectors=None,
    figsize=(12, 7.5),
):
    fig, ax = plt.subplots(figsize=figsize, dpi=250)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    # Banner
    ax.text(50, 96.5, title, ha="center", va="center", fontsize=16, fontweight="bold", color="#0F172A")
    ax.text(50, 93.5, subtitle, ha="center", va="center", fontsize=10.5, color="#475569")

    # Draw Tables
    for tbl in tables:
        x, y, w, h = tbl["pos"]
        name = tbl["name"]
        columns = tbl["cols"]

        # Outer card
        card = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.25,rounding_size=0.5",
            facecolor="#FFFFFF",
            edgecolor=border_color,
            linewidth=1.8,
            zorder=3,
        )
        ax.add_patch(card)

        # Header box
        header_h = 2.4
        hdr = patches.FancyBboxPatch(
            (x, y + h - header_h),
            w,
            header_h,
            boxstyle="round,pad=0.25,rounding_size=0.5",
            facecolor=header_color,
            edgecolor=header_color,
            linewidth=1.2,
            zorder=4,
        )
        ax.add_patch(hdr)

        ax.text(
            x + w / 2,
            y + h - header_h / 2,
            name,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color="#FFFFFF",
            zorder=5,
        )

        spacing = (h - header_h - 0.8) / max(len(columns), 1)
        curr_y = y + h - header_h - 0.7

        for col in columns:
            is_pk = "[PK]" in col
            is_fk = "[FK]" in col

            if is_pk and is_fk:
                txt_color = "#B45309"
                weight = "bold"
            elif is_pk:
                txt_color = "#1D4ED8"
                weight = "bold"
            elif is_fk:
                txt_color = "#6D28D9"
                weight = "semibold"
            elif "---" in col:
                txt_color = "#64748B"
                weight = "bold"
            else:
                txt_color = "#0F172A"
                weight = "normal"

            font_sz = 9.8 if "---" not in col else 8.5
            ax.text(
                x + 0.6,
                curr_y,
                col,
                ha="left",
                va="center",
                fontsize=font_sz,
                fontweight=weight,
                color=txt_color,
                zorder=5,
            )
            curr_y -= spacing

    # Draw Connectors
    if connectors:
        for p1, p2, label, lpos in connectors:
            ax.annotate(
                "",
                xy=p2,
                xytext=p1,
                arrowprops=dict(arrowstyle="-|>", color="#334155", lw=1.6, mutation_scale=12),
                zorder=6,
            )
            if label and lpos:
                ax.text(
                    lpos[0],
                    lpos[1],
                    label,
                    fontsize=8.5,
                    fontweight="bold",
                    color="#1E293B",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#CBD5E1", alpha=0.9),
                    zorder=7,
                )

    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight", dpi=250)
    plt.close()
    print(f"Generated {filename} successfully!")


def build_all_domain_diagrams():
    # --- 1. Identity & Access Control ---
    generate_domain_diagram(
        filename="schema_d1_identity.png",
        title="Domain 1: Identity & Access Control - Physical Schema",
        subtitle="User authentication, system roles, composite role assignment, and administrator approval history",
        header_color="#1E3A8A",
        border_color="#3B82F6",
        figsize=(13, 8.5),
        tables=[
            {
                "name": "users (Entity)",
                "pos": (3.0, 48.0, 29.0, 40.0),
                "cols": [
                    "[PK] user_id: INTEGER (SERIAL)",
                    "username: VARCHAR(50) NULL (UQ)",
                    "email: VARCHAR(255) NOT NULL (UQ)",
                    "password_hash: VARCHAR(255) NOT NULL",
                    "account_status: VARCHAR(50) NOT NULL",
                    "  DEFAULT 'active'",
                    "created_at: TIMESTAMPTZ NOT NULL",
                    "--- Constraints & Indexes ---",
                    "UNIQUE (email), UNIQUE (username)",
                    "INDEX (user_id), INDEX (email)",
                ],
            },
            {
                "name": "roles (Lookup Entity)",
                "pos": (38.0, 52.0, 27.0, 36.0),
                "cols": [
                    "[PK] role_id: INTEGER (SERIAL)",
                    "name: VARCHAR(50) NOT NULL (UQ)",
                    "--- Constraints ---",
                    "UNIQUE (name)",
                    "INDEX (role_id), INDEX (name)",
                    "--- Values ---",
                    "• student",
                    "• lecturer",
                    "• administrator",
                ],
            },
            {
                "name": "user_roles (Associative Junction)",
                "pos": (69.0, 48.0, 28.0, 40.0),
                "cols": [
                    "[PK][FK] user_id: INT (users)",
                    "[PK][FK] role_id: INT (roles)",
                    "assigned_at: TIMESTAMPTZ NOT NULL",
                    "[FK] assigned_by: INT NULL (users)",
                    "--- Composite PK ---",
                    "(user_id, role_id)",
                    "--- Referential Actions ---",
                    "FK user_id ON DELETE CASCADE",
                    "FK role_id ON DELETE CASCADE",
                    "FK assigned_by ON DELETE SET NULL",
                ],
            },
            {
                "name": "lecturer_approval_events (Audit Entity)",
                "pos": (20.0, 6.0, 60.0, 36.0),
                "cols": [
                    "[PK] approval_id: INTEGER (SERIAL)",
                    "[FK] lecturer_user_id: INTEGER NOT NULL (users.user_id)",
                    "[FK] administrator_user_id: INTEGER NOT NULL (users.user_id)",
                    "decision: VARCHAR(50) NOT NULL",
                    "decided_at: TIMESTAMPTZ NOT NULL DEFAULT now()",
                    "--- Integrity Constraints & Cascades ---",
                    "CHECK (decision IN ('approved', 'rejected'))",
                    "FK lecturer_user_id ON DELETE CASCADE",
                    "FK administrator_user_id ON DELETE RESTRICT (Preserves admin review audit)",
                ],
            },
        ],
        connectors=[
            ((32.0, 68.0), (69.0, 68.0), "1 : N (user_roles.user_id)", (48.0, 69.5)),
            ((65.0, 70.0), (69.0, 70.0), "1 : N (user_roles.role_id)", (65.5, 71.5)),
            ((17.5, 48.0), (28.0, 42.0), "1:N (lecturer)", (16.0, 44.0)),
            ((25.0, 48.0), (45.0, 42.0), "1:N (admin)", (34.0, 44.0)),
        ],
    )

    # --- 2. Courses & Materials ---
    generate_domain_diagram(
        filename="schema_d2_courses.png",
        title="Domain 2: Courses, Prerequisite Map & Materials - Physical Schema",
        subtitle="Course catalogue, student enrolments, prerequisite graph, and extracted document passages",
        header_color="#065F46",
        border_color="#10B981",
        figsize=(14, 9.5),
        tables=[
            {
                "name": "courses (Entity)",
                "pos": (2.0, 52.0, 30.0, 38.0),
                "cols": [
                    "[PK] course_id: INTEGER (SERIAL)",
                    "title: VARCHAR(255) NOT NULL",
                    "[FK] owner_user_id: INT (users)",
                    "ai_enabled: BOOLEAN NOT NULL",
                    "  DEFAULT true",
                    "--- Foreign Key Actions ---",
                    "FK owner_user_id ON DELETE RESTRICT",
                    "INDEX (course_id), INDEX (title)",
                ],
            },
            {
                "name": "enrolments (Junction)",
                "pos": (35.0, 56.0, 29.0, 34.0),
                "cols": [
                    "[PK][FK] course_id: INT (courses)",
                    "[PK][FK] user_id: INT (users)",
                    "status: VARCHAR(50) NOT NULL",
                    "enrolled_at: TIMESTAMPTZ NOT NULL",
                    "--- Composite PK ---",
                    "(course_id, user_id)",
                    "FK course_id CASCADE",
                    "FK user_id CASCADE",
                ],
            },
            {
                "name": "concepts (Entity)",
                "pos": (67.0, 52.0, 31.0, 38.0),
                "cols": [
                    "[PK] concept_id: INTEGER (SERIAL)",
                    "[FK] course_id: INT (courses)",
                    "name: VARCHAR(255) NOT NULL",
                    "--- Constraints ---",
                    "UNIQUE (course_id, name)",
                    "FK course_id ON DELETE CASCADE",
                    "INDEX (concept_id), INDEX (course_id)",
                ],
            },
            {
                "name": "materials (Document Entity)",
                "pos": (2.0, 6.0, 30.0, 40.0),
                "cols": [
                    "[PK] material_id: INTEGER (SERIAL)",
                    "[FK] course_id: INT (courses)",
                    "[FK] uploaded_by: INT (users)",
                    "file_path: VARCHAR(512) NOT NULL",
                    "processing_status: VARCHAR(50)",
                    "uploaded_at: TIMESTAMPTZ NOT NULL",
                    "--- Foreign Keys ---",
                    "FK course_id ON DELETE CASCADE",
                    "FK uploaded_by ON DELETE RESTRICT",
                ],
            },
            {
                "name": "material_sections (Passages)",
                "pos": (35.0, 6.0, 30.0, 44.0),
                "cols": [
                    "[PK] section_id: INTEGER (SERIAL)",
                    "[FK] material_id: INT (materials)",
                    "section_order: INT NOT NULL",
                    "text: TEXT NOT NULL",
                    "source_location_type: VARCHAR(50)",
                    "source_location_value: VARCHAR(100)",
                    "--- Constraints ---",
                    "UNIQUE (material_id, section_order)",
                    "FK material_id ON DELETE CASCADE",
                ],
            },
            {
                "name": "concept_prerequisites (Graph)",
                "pos": (67.0, 6.0, 31.0, 42.0),
                "cols": [
                    "[PK][FK] concept_id: INT",
                    "[PK][FK] prereq_concept_id: INT",
                    "--- Integrity Checks ---",
                    "CHECK (concept_id != prereq)",
                    "Composite PK (concept, prereq)",
                    "FK concept_id CASCADE",
                    "FK prereq_concept_id CASCADE",
                ],
            },
        ],
        connectors=[
            ((32.0, 71.0), (35.0, 71.0), "1:N", (32.5, 72.5)),
            ((32.0, 78.0), (67.0, 78.0), "1:N (Course Concepts)", (47.0, 79.5)),
            ((17.0, 52.0), (17.0, 46.0), "1:N", (17.5, 48.5)),
            ((32.0, 24.0), (35.0, 24.0), "1:N (Sections)", (32.5, 25.5)),
            ((82.5, 52.0), (82.5, 48.0), "1:N (Prereqs)", (83.0, 49.5)),
        ],
    )

    # --- 3. Assessment & Grading ---
    generate_domain_diagram(
        filename="schema_d3_assessment.png",
        title="Domain 3: Assessment, Questions & Grading - Physical Schema",
        subtitle="Assignments, release gating, question scoring, student submissions, and formative marks",
        header_color="#9A3412",
        border_color="#F97316",
        figsize=(14, 9.0),
        tables=[
            {
                "name": "assignments (Entity)",
                "pos": (2.0, 48.0, 31.0, 42.0),
                "cols": [
                    "[PK] assignment_id: INTEGER (SERIAL)",
                    "[FK] course_id: INTEGER (courses)",
                    "title: VARCHAR(255) NOT NULL",
                    "due_at: TIMESTAMPTZ NOT NULL",
                    "lifecycle_status: VARCHAR(50) NOT NULL",
                    "results_released_at: TIMESTAMPTZ NULL",
                    "[FK] results_released_by: INT NULL",
                    "cmb_enabled: BOOLEAN DEFAULT true",
                    "--- Foreign Keys ---",
                    "FK course_id ON DELETE CASCADE",
                    "FK results_released_by SET NULL",
                ],
            },
            {
                "name": "assignment_questions (Entity)",
                "pos": (36.0, 52.0, 31.0, 38.0),
                "cols": [
                    "[PK] question_id: INTEGER (SERIAL)",
                    "[FK] assignment_id: INT (assignments)",
                    "prompt: TEXT NOT NULL",
                    "max_score: NUMERIC(5,2) NOT NULL",
                    "position: INTEGER NOT NULL",
                    "--- Constraints ---",
                    "UNIQUE (assignment_id, position)",
                    "FK assignment_id ON DELETE CASCADE",
                ],
            },
            {
                "name": "question_concepts (Junction)",
                "pos": (70.0, 56.0, 28.0, 30.0),
                "cols": [
                    "[PK][FK] question_id: INT",
                    "[PK][FK] concept_id: INT",
                    "--- Composite PK ---",
                    "(question_id, concept_id)",
                    "FK question_id CASCADE",
                    "FK concept_id CASCADE",
                ],
            },
            {
                "name": "submissions (Entity)",
                "pos": (2.0, 6.0, 31.0, 38.0),
                "cols": [
                    "[PK] submission_id: INTEGER (SERIAL)",
                    "[FK] assignment_id: INT (assignments)",
                    "[FK] user_id: INT (users)",
                    "submitted_at: TIMESTAMPTZ NOT NULL",
                    "work_reference: VARCHAR(512) NOT NULL",
                    "marking_status: VARCHAR(50) NOT NULL",
                    "--- Constraints ---",
                    "UNIQUE (assignment_id, user_id)",
                    "FK assignment_id CASCADE, FK user_id CASCADE",
                ],
            },
            {
                "name": "marks (Question Evaluations)",
                "pos": (36.0, 6.0, 31.0, 42.0),
                "cols": [
                    "[PK][FK] submission_id: INT (submissions)",
                    "[PK][FK] question_id: INT (questions)",
                    "score: NUMERIC(5,2) NOT NULL",
                    "lecturer_comment: TEXT NULL",
                    "[FK] graded_by: INT (users) NOT NULL",
                    "graded_at: TIMESTAMPTZ NOT NULL",
                    "--- Composite PK ---",
                    "(submission_id, question_id)",
                    "FK submission_id CASCADE",
                    "FK question_id CASCADE, FK graded_by RESTRICT",
                ],
            },
        ],
        connectors=[
            ((33.0, 71.0), (36.0, 71.0), "1:N Questions", (33.5, 72.5)),
            ((67.0, 71.0), (70.0, 71.0), "M:N Concepts", (67.2, 72.5)),
            ((17.5, 48.0), (17.5, 44.0), "1:N Submissions", (18.0, 45.5)),
            ((33.0, 25.0), (36.0, 25.0), "1:1 Mark", (33.5, 26.5)),
            ((51.5, 52.0), (51.5, 48.0), "1:N Marks", (52.0, 49.5)),
        ],
    )

    # --- 4. Concept-to-Mastery Bridge (CMB) ---
    generate_domain_diagram(
        filename="schema_d4_cmb.png",
        title="Domain 4: Concept-to-Mastery Bridge (CMB) Engine - Physical Schema",
        subtitle="Question bank, diagnostic sessions, responses with confidence, hypotheses, interventions, and verification",
        header_color="#581C87",
        border_color="#A855F7",
        figsize=(14.5, 10.0),
        tables=[
            {
                "name": "cmb_items (Item Bank)",
                "pos": (2.0, 52.0, 30.0, 40.0),
                "cols": [
                    "[PK] item_id: INTEGER (SERIAL)",
                    "[FK] course_id: INTEGER (courses)",
                    "item_type: VARCHAR(50) NOT NULL",
                    "  CHECK IN ('diagnostic',",
                    "            'practice', 'verification')",
                    "prompt: TEXT NOT NULL",
                    "review_status: VARCHAR(50) NOT NULL",
                    "[FK] approved_by: INT NULL (users)",
                    "FK course_id CASCADE, FK approved_by SET NULL",
                ],
            },
            {
                "name": "diagnostic_sessions (Entity)",
                "pos": (35.0, 56.0, 31.0, 36.0),
                "cols": [
                    "[PK] session_id: INTEGER (SERIAL)",
                    "[FK] submission_id: INT (submissions)",
                    "started_at: TIMESTAMPTZ NOT NULL",
                    "completed_at: TIMESTAMPTZ NULL",
                    "--- Gated Access ---",
                    "Requires released results",
                    "FK submission_id ON DELETE CASCADE",
                ],
            },
            {
                "name": "responses (Student Evidence)",
                "pos": (69.0, 50.0, 29.0, 42.0),
                "cols": [
                    "[PK] response_id: INTEGER (SERIAL)",
                    "[FK] session_id: INT (sessions)",
                    "[FK] item_id: INT (cmb_items)",
                    "answer: TEXT NOT NULL",
                    "confidence_choice: VARCHAR(50)",
                    "response_time: INTEGER (seconds)",
                    "--- Foreign Keys ---",
                    "FK session_id ON DELETE CASCADE",
                    "FK item_id ON DELETE RESTRICT",
                ],
            },
            {
                "name": "candidate_explanations (Hypotheses)",
                "pos": (2.0, 6.0, 31.0, 42.0),
                "cols": [
                    "[PK] explanation_id: INT (SERIAL)",
                    "[FK] session_id: INT (sessions)",
                    "[FK] concept_id: INT (concepts)",
                    "label: VARCHAR(255) NOT NULL",
                    "confidence: FLOAT NOT NULL (0.0 - 1.0)",
                    "--- Reasoning Note ---",
                    "Stored as hypotheses, never facts",
                    "FK session_id CASCADE, FK concept_id CASCADE",
                ],
            },
            {
                "name": "interventions (Remediation)",
                "pos": (36.0, 8.0, 29.0, 34.0),
                "cols": [
                    "[PK] intervention_id: INT (SERIAL)",
                    "[FK] explanation_id: INT (explanations)",
                    "--- Remediation Blueprint ---",
                    "Connects diagnosis to support",
                    "FK explanation_id ON DELETE CASCADE",
                ],
            },
            {
                "name": "recommended_resources (Passages)",
                "pos": (68.0, 6.0, 30.0, 38.0),
                "cols": [
                    "[PK][FK] intervention_id: INT",
                    "[PK][FK] section_id: INT (sections)",
                    "reason: TEXT NULL",
                    "--- Composite PK ---",
                    "(intervention_id, section_id)",
                    "FK intervention_id CASCADE",
                    "FK section_id CASCADE",
                ],
            },
        ],
        connectors=[
            ((50.5, 56.0), (50.5, 48.0), "1:N Responses", (51.0, 50.0)),
            ((35.0, 65.0), (17.5, 48.0), "1:N Hypotheses", (22.0, 54.0)),
            ((33.0, 24.0), (36.0, 24.0), "1:N Plan", (33.5, 25.5)),
            ((65.0, 24.0), (68.0, 24.0), "1:N Passages", (65.5, 25.5)),
        ],
    )

    # --- 5. Audit & AI Gateway ---
    generate_domain_diagram(
        filename="schema_d5_audit.png",
        title="Domain 5: Security Audit Trail & AI Gateway - Physical Schema",
        subtitle="Polymorphic security activity logging, AI Gateway request tracking, and grounding source citations",
        header_color="#334155",
        border_color="#64748B",
        figsize=(13.5, 8.5),
        tables=[
            {
                "name": "access_logs (Polymorphic Audit)",
                "pos": (3.0, 16.0, 30.0, 72.0),
                "cols": [
                    "[PK] log_id: INTEGER (SERIAL)",
                    "[FK] user_id: INTEGER NULL (users)",
                    "action: VARCHAR(100) NOT NULL",
                    "target_type: VARCHAR(100) NOT NULL",
                    "target_id: VARCHAR(100) NOT NULL",
                    "occurred_at: TIMESTAMPTZ NOT NULL",
                    "  DEFAULT now()",
                    "--- Polymorphic Design ---",
                    "target_type / target_id captures:",
                    "• 'submission', 'course', 'session'",
                    "--- Audit Preservation ---",
                    "FK user_id ON DELETE SET NULL",
                    "(Logs preserved on user deletion)",
                    "INDEX (log_id), INDEX (user_id)",
                    "INDEX (action), INDEX (occurred_at)",
                ],
            },
            {
                "name": "ai_gateway_requests (Gateway Log)",
                "pos": (37.0, 24.0, 30.0, 64.0),
                "cols": [
                    "[PK] request_id: INTEGER (SERIAL)",
                    "[FK] user_id: INTEGER (users)",
                    "[FK] course_id: INTEGER (courses)",
                    "purpose: VARCHAR(100) NOT NULL",
                    "provider: VARCHAR(100) NOT NULL",
                    "status: VARCHAR(50) NOT NULL",
                    "created_at: TIMESTAMPTZ NOT NULL",
                    "--- Privacy Invariants ---",
                    "• Only egress path to external LLMs",
                    "• Enforces course.ai_enabled toggle",
                    "• Strips student identifiable info",
                    "FK user_id ON DELETE RESTRICT",
                    "FK course_id ON DELETE CASCADE",
                ],
            },
            {
                "name": "ai_gateway_request_sources (Grounding)",
                "pos": (70.0, 32.0, 27.0, 48.0),
                "cols": [
                    "[PK][FK] request_id: INT (ai_req)",
                    "[PK][FK] section_id: INT (sections)",
                    "--- Grounding Invariant ---",
                    "Records exact lecturer sections",
                    "sent to external LLM context",
                    "--- Composite PK ---",
                    "(request_id, section_id)",
                    "FK request_id CASCADE",
                    "FK section_id CASCADE",
                ],
            },
        ],
        connectors=[
            ((67.0, 56.0), (70.0, 56.0), "1:N Grounding", (67.2, 57.5)),
        ],
    )


if __name__ == "__main__":
    build_all_domain_diagrams()
