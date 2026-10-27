"""Generate crystal-clear, large-font database diagrams optimized for print at 6.6 inches wide.

Design philosophy: FEWER items per diagram, BIGGER fonts, MORE whitespace.
Each domain gets its own focused diagram with 14-18pt headers and 11-12pt body text.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def make_table_box(ax, x, y, w, name, columns, header_color, border_color):
    """Draw a single table box with large, readable fonts."""
    row_h = 1.8  # height per row
    header_h = 2.5
    h = header_h + len(columns) * row_h + 0.6

    # Card background
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.3,rounding_size=0.5",
        facecolor="#FFFFFF", edgecolor=border_color, linewidth=2.2, zorder=3,
    )
    ax.add_patch(card)

    # Header bar
    hdr = patches.FancyBboxPatch(
        (x, y + h - header_h), w, header_h,
        boxstyle="round,pad=0.3,rounding_size=0.5",
        facecolor=header_color, edgecolor=header_color, linewidth=1.5, zorder=4,
    )
    ax.add_patch(hdr)

    # Table name - LARGE
    ax.text(x + w / 2, y + h - header_h / 2, name,
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="white", zorder=5)

    # Column rows
    cy = y + h - header_h - 0.3
    for col_text in columns:
        cy -= row_h
        is_pk = col_text.startswith("PK")
        is_fk = "FK" in col_text and not is_pk
        is_pkfk = col_text.startswith("PK,FK") or col_text.startswith("PK/FK")

        if is_pkfk:
            color = "#B45309"
            weight = "bold"
            icon = "[PK/FK] "
        elif is_pk:
            color = "#1D4ED8"
            weight = "bold"
            icon = "[PK] "
        elif is_fk:
            color = "#7C3AED"
            weight = "bold"
            icon = "[FK] "
        else:
            color = "#1E293B"
            weight = "normal"
            icon = "    "

        ax.text(x + 0.8, cy + row_h * 0.45, f"{icon}{col_text}",
                ha="left", va="center", fontsize=11, fontweight=weight,
                color=color, zorder=5)

    return h


def draw_arrow(ax, x1, y1, x2, y2, label=None, color="#475569"):
    """Draw a labeled relationship arrow."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0,
                                mutation_scale=14),
                zorder=6)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.6, label, ha="center", va="center",
                fontsize=10, fontweight="bold", color=color,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color,
                          lw=1.2, alpha=0.95),
                zorder=7)


# ─────────────────────────────────────────────
# DIAGRAM 1: Identity & Access Control
# ─────────────────────────────────────────────
def gen_d1():
    fig, ax = plt.subplots(figsize=(10, 11), dpi=200)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 55)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(25, 53.5, "Domain 1: Identity & Access Control",
            ha="center", fontsize=18, fontweight="bold", color="#1E3A8A")
    ax.text(25, 51.8, "Users, Roles, Role Assignments & Lecturer Approval Audit",
            ha="center", fontsize=12, color="#64748B")

    HC, BC = "#1E3A8A", "#3B82F6"

    make_table_box(ax, 1, 32, 22, "users", [
        "PK  user_id : INTEGER (SERIAL)",
        "    username : VARCHAR(50) UNIQUE",
        "    email : VARCHAR(255) NOT NULL UNIQUE",
        "    password_hash : VARCHAR(255)",
        "    account_status : VARCHAR(50)",
        "    created_at : TIMESTAMPTZ",
    ], HC, BC)

    make_table_box(ax, 27, 36, 22, "roles", [
        "PK  role_id : INTEGER (SERIAL)",
        "    name : VARCHAR(50) UNIQUE",
        "    (student | lecturer | admin)",
    ], HC, BC)

    make_table_box(ax, 27, 17, 22, "user_roles", [
        "PK,FK  user_id → users",
        "PK,FK  role_id → roles",
        "    assigned_at : TIMESTAMPTZ",
        "FK  assigned_by → users (SET NULL)",
    ], HC, BC)

    make_table_box(ax, 1, 5, 22, "lecturer_approval_events", [
        "PK  approval_id : INTEGER (SERIAL)",
        "FK  lecturer_user_id → users (CASCADE)",
        "FK  admin_user_id → users (RESTRICT)",
        "    decision : 'approved' | 'rejected'",
        "    decided_at : TIMESTAMPTZ",
    ], HC, BC)

    draw_arrow(ax, 23, 40, 27, 26, "1 : N", BC)
    draw_arrow(ax, 38, 36, 38, 30, "1 : N", BC)
    draw_arrow(ax, 12, 32, 12, 21, "1 : N", BC)

    ax.text(25, 1.5,
            "Legend:  [PK] = Primary Key  |  [FK] = Foreign Key  |  CASCADE / RESTRICT / SET NULL = Delete Behavior",
            ha="center", fontsize=9.5, color="#64748B")

    plt.tight_layout()
    plt.savefig("schema_d1_identity.png", bbox_inches="tight", dpi=200)
    plt.close()
    print("✓ schema_d1_identity.png")


# ─────────────────────────────────────────────
# DIAGRAM 2: Courses & Materials
# ─────────────────────────────────────────────
def gen_d2():
    fig, ax = plt.subplots(figsize=(10, 14), dpi=200)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 70)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(25, 68.5, "Domain 2: Courses, Concepts & Materials",
            ha="center", fontsize=18, fontweight="bold", color="#065F46")
    ax.text(25, 66.8, "Course Catalogue, Enrolments, Prerequisite Graph & Extracted Passages",
            ha="center", fontsize=12, color="#64748B")

    HC, BC = "#065F46", "#10B981"

    make_table_box(ax, 1, 51, 22, "courses", [
        "PK  course_id : INTEGER (SERIAL)",
        "    title : VARCHAR(255) NOT NULL",
        "FK  owner_user_id → users (RESTRICT)",
        "    ai_enabled : BOOLEAN DEFAULT true",
    ], HC, BC)

    make_table_box(ax, 27, 53, 22, "enrolments", [
        "PK,FK  course_id → courses",
        "PK,FK  user_id → users",
        "    status : VARCHAR(50)",
        "    enrolled_at : TIMESTAMPTZ",
    ], HC, BC)

    make_table_box(ax, 1, 35, 22, "concepts", [
        "PK  concept_id : INTEGER (SERIAL)",
        "FK  course_id → courses (CASCADE)",
        "    name : VARCHAR(255) NOT NULL",
        "    UNIQUE(course_id, name)",
    ], HC, BC)

    make_table_box(ax, 27, 37, 22, "concept_prerequisites", [
        "PK,FK  concept_id → concepts",
        "PK,FK  prereq_concept_id → concepts",
        "    CHECK(concept ≠ prerequisite)",
    ], HC, BC)

    make_table_box(ax, 1, 16, 22, "materials", [
        "PK  material_id : INTEGER (SERIAL)",
        "FK  course_id → courses (CASCADE)",
        "FK  uploaded_by → users (RESTRICT)",
        "    file_path : VARCHAR(512)",
        "    processing_status : VARCHAR(50)",
        "    uploaded_at : TIMESTAMPTZ",
    ], HC, BC)

    make_table_box(ax, 27, 14, 22, "material_sections", [
        "PK  section_id : INTEGER (SERIAL)",
        "FK  material_id → materials (CASCADE)",
        "    section_order : INT NOT NULL",
        "    text : TEXT NOT NULL",
        "    source_location_type : VARCHAR(50)",
        "    source_location_value : VARCHAR(100)",
        "    UNIQUE(material_id, section_order)",
    ], HC, BC)

    make_table_box(ax, 14, 1, 22, "material_section_concepts", [
        "PK,FK  section_id → material_sections",
        "PK,FK  concept_id → concepts",
    ], HC, BC)

    draw_arrow(ax, 23, 57, 27, 57, "1 : N", BC)
    draw_arrow(ax, 12, 51, 12, 47.5, "1 : N", BC)
    draw_arrow(ax, 23, 42, 27, 42, "1 : N", BC)
    draw_arrow(ax, 12, 35, 12, 30, "1 : N", BC)
    draw_arrow(ax, 23, 24, 27, 28, "1 : N", BC)

    plt.tight_layout()
    plt.savefig("schema_d2_courses.png", bbox_inches="tight", dpi=200)
    plt.close()
    print("✓ schema_d2_courses.png")


# ─────────────────────────────────────────────
# DIAGRAM 3: Assessment & Grading
# ─────────────────────────────────────────────
def gen_d3():
    fig, ax = plt.subplots(figsize=(10, 13), dpi=200)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 65)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(25, 63.5, "Domain 3: Assessment & Grading Lifecycle",
            ha="center", fontsize=18, fontweight="bold", color="#9A3412")
    ax.text(25, 61.8, "Assignments, Questions, Submissions & Question-Level Marks",
            ha="center", fontsize=12, color="#64748B")

    HC, BC = "#9A3412", "#F97316"

    make_table_box(ax, 1, 43, 22, "assignments", [
        "PK  assignment_id : INTEGER (SERIAL)",
        "FK  course_id → courses (CASCADE)",
        "    title : VARCHAR(255) NOT NULL",
        "    due_at : TIMESTAMPTZ NOT NULL",
        "    lifecycle_status : VARCHAR(50)",
        "    results_released_at : TIMESTAMPTZ",
        "FK  results_released_by → users",
        "    cmb_enabled : BOOLEAN DEFAULT true",
    ], HC, BC)

    make_table_box(ax, 27, 47, 22, "assignment_questions", [
        "PK  question_id : INTEGER (SERIAL)",
        "FK  assignment_id → assignments",
        "    prompt : TEXT NOT NULL",
        "    max_score : NUMERIC(5,2)",
        "    position : INT NOT NULL",
        "    UNIQUE(assignment_id, position)",
    ], HC, BC)

    make_table_box(ax, 1, 18, 22, "submissions", [
        "PK  submission_id : INTEGER (SERIAL)",
        "FK  assignment_id → assignments",
        "FK  user_id → users (CASCADE)",
        "    submitted_at : TIMESTAMPTZ",
        "    work_reference : VARCHAR(512)",
        "    marking_status : VARCHAR(50)",
        "    UNIQUE(assignment_id, user_id)",
    ], HC, BC)

    make_table_box(ax, 27, 22, 22, "marks", [
        "PK,FK  submission_id → submissions",
        "PK,FK  question_id → questions",
        "    score : NUMERIC(5,2) NOT NULL",
        "    lecturer_comment : TEXT",
        "FK  graded_by → users (RESTRICT)",
        "    graded_at : TIMESTAMPTZ",
    ], HC, BC)

    make_table_box(ax, 27, 6, 22, "question_concepts", [
        "PK,FK  question_id → questions",
        "PK,FK  concept_id → concepts",
    ], HC, BC)

    draw_arrow(ax, 23, 55, 27, 55, "1 : N", BC)
    draw_arrow(ax, 12, 43, 12, 33, "1 : N", BC)
    draw_arrow(ax, 23, 28, 27, 32, "1 : N", BC)
    draw_arrow(ax, 38, 47, 38, 37, "1 : N", BC)

    plt.tight_layout()
    plt.savefig("schema_d3_assessment.png", bbox_inches="tight", dpi=200)
    plt.close()
    print("✓ schema_d3_assessment.png")


# ─────────────────────────────────────────────
# DIAGRAM 4a: CMB Engine - Top Half (Diagnosis)
# ─────────────────────────────────────────────
def gen_d4a():
    fig, ax = plt.subplots(figsize=(10, 11), dpi=200)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 55)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(25, 53.5, "Domain 4a: CMB Engine — Diagnosis Phase",
            ha="center", fontsize=18, fontweight="bold", color="#581C87")
    ax.text(25, 51.8, "Item Bank, Diagnostic Sessions, Student Responses & Hypotheses",
            ha="center", fontsize=12, color="#64748B")

    HC, BC = "#581C87", "#A855F7"

    make_table_box(ax, 1, 33, 22, "cmb_items (Item Bank)", [
        "PK  item_id : INTEGER (SERIAL)",
        "FK  course_id → courses (CASCADE)",
        "    item_type : diagnostic|practice|verif",
        "    prompt : TEXT NOT NULL",
        "    review_status : VARCHAR(50)",
        "FK  approved_by → users (SET NULL)",
    ], HC, BC)

    make_table_box(ax, 27, 35, 22, "diagnostic_sessions", [
        "PK  session_id : INTEGER (SERIAL)",
        "FK  submission_id → submissions",
        "    started_at : TIMESTAMPTZ",
        "    completed_at : TIMESTAMPTZ",
        "    (Gated: requires released results)",
    ], HC, BC)

    make_table_box(ax, 1, 10, 22, "responses", [
        "PK  response_id : INTEGER (SERIAL)",
        "FK  session_id → sessions (CASCADE)",
        "FK  item_id → cmb_items (RESTRICT)",
        "    answer : TEXT NOT NULL",
        "    confidence_choice : VARCHAR(50)",
        "    response_time : INTEGER (seconds)",
    ], HC, BC)

    make_table_box(ax, 27, 10, 22, "candidate_explanations", [
        "PK  explanation_id : INT (SERIAL)",
        "FK  session_id → sessions (CASCADE)",
        "FK  concept_id → concepts (CASCADE)",
        "    label : VARCHAR(255)",
        "    confidence : FLOAT (0.0 – 1.0)",
        "    (Hypotheses, never absolute facts)",
    ], HC, BC)

    draw_arrow(ax, 38, 35, 12, 24, "1 : N", BC)
    draw_arrow(ax, 38, 35, 38, 24, "1 : N", BC)

    plt.tight_layout()
    plt.savefig("schema_d4a_cmb_diagnosis.png", bbox_inches="tight", dpi=200)
    plt.close()
    print("✓ schema_d4a_cmb_diagnosis.png")


# ─────────────────────────────────────────────
# DIAGRAM 4b: CMB Engine - Bottom Half (Remediation)
# ─────────────────────────────────────────────
def gen_d4b():
    fig, ax = plt.subplots(figsize=(10, 10), dpi=200)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(25, 48.5, "Domain 4b: CMB Engine — Remediation & Verification",
            ha="center", fontsize=18, fontweight="bold", color="#581C87")
    ax.text(25, 46.8, "Interventions, Recommended Reading Passages & Follow-Up Verification",
            ha="center", fontsize=12, color="#64748B")

    HC, BC = "#581C87", "#A855F7"

    make_table_box(ax, 14, 33, 22, "interventions", [
        "PK  intervention_id : INT (SERIAL)",
        "FK  explanation_id → explanations",
        "    (Targeted remediation plan)",
    ], HC, BC)

    make_table_box(ax, 1, 13, 22, "recommended_resources", [
        "PK,FK  intervention_id → interventions",
        "PK,FK  section_id → material_sections",
        "    reason : TEXT",
        "    (Links to lecturer-authored passages)",
    ], HC, BC)

    make_table_box(ax, 27, 13, 22, "followup_results", [
        "PK  followup_id : INTEGER (SERIAL)",
        "FK  intervention_id → interventions",
        "FK  item_id → cmb_items (RESTRICT)",
        "    correct : BOOLEAN NOT NULL",
        "    answered_at : TIMESTAMPTZ",
        "    (Uses fresh verification item)",
    ], HC, BC)

    make_table_box(ax, 14, 1, 22, "cmb_item_concepts", [
        "PK,FK  item_id → cmb_items",
        "PK,FK  concept_id → concepts",
    ], HC, BC)

    draw_arrow(ax, 20, 33, 12, 25, "1 : N", BC)
    draw_arrow(ax, 30, 33, 38, 27, "1 : N", BC)

    plt.tight_layout()
    plt.savefig("schema_d4b_cmb_remediation.png", bbox_inches="tight", dpi=200)
    plt.close()
    print("✓ schema_d4b_cmb_remediation.png")


# ─────────────────────────────────────────────
# DIAGRAM 5: Audit & AI Gateway
# ─────────────────────────────────────────────
def gen_d5():
    fig, ax = plt.subplots(figsize=(10, 11), dpi=200)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 55)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(25, 53.5, "Domain 5: Security Audit Trail & AI Gateway",
            ha="center", fontsize=18, fontweight="bold", color="#334155")
    ax.text(25, 51.8, "Polymorphic Activity Logs, AI Request Tracking & Grounding Citations",
            ha="center", fontsize=12, color="#64748B")

    HC, BC = "#334155", "#64748B"

    make_table_box(ax, 1, 28, 22, "access_logs", [
        "PK  log_id : INTEGER (SERIAL)",
        "FK  user_id → users (SET NULL)",
        "    action : VARCHAR(100) NOT NULL",
        "    target_type : VARCHAR(100)",
        "    target_id : VARCHAR(100)",
        "    occurred_at : TIMESTAMPTZ",
        "    (Polymorphic audit — preserved",
        "     even after user deletion)",
    ], HC, BC)

    make_table_box(ax, 27, 30, 22, "ai_gateway_requests", [
        "PK  request_id : INTEGER (SERIAL)",
        "FK  user_id → users (RESTRICT)",
        "FK  course_id → courses (CASCADE)",
        "    purpose : VARCHAR(100)",
        "    provider : VARCHAR(100)",
        "    status : VARCHAR(50)",
        "    created_at : TIMESTAMPTZ",
    ], HC, BC)

    make_table_box(ax, 14, 8, 22, "ai_gateway_request_sources", [
        "PK,FK  request_id → ai_gateway_requests",
        "PK,FK  section_id → material_sections",
        "    (Records exact lecturer passages",
        "     sent to external LLM context)",
    ], HC, BC)

    draw_arrow(ax, 38, 30, 25, 20, "1 : N", BC)

    plt.tight_layout()
    plt.savefig("schema_d5_audit.png", bbox_inches="tight", dpi=200)
    plt.close()
    print("✓ schema_d5_audit.png")


# ─────────────────────────────────────────────
# MASTER ER OVERVIEW (Simplified, Large Font)
# ─────────────────────────────────────────────
def gen_er_overview():
    fig, ax = plt.subplots(figsize=(10, 13), dpi=200)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 65)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(25, 63.5, "LMS Entity-Relationship Overview",
            ha="center", fontsize=18, fontweight="bold", color="#0F172A")
    ax.text(25, 61.8, "Conceptual Domain Map with Key Relationships & Cardinalities",
            ha="center", fontsize=12, color="#64748B")

    # Domain boxes (simplified — entity names only, large font)
    domain_data = [
        (1, 47, 22, 13, "Domain 1: Identity", "#EFF6FF", "#3B82F6",
         ["User", "Role", "UserRole (M:N)", "LecturerApprovalEvent"]),
        (27, 47, 22, 13, "Domain 2: Courses", "#ECFDF5", "#10B981",
         ["Course", "Enrolment (M:N)", "Concept → Prerequisites",
          "Material → Sections"]),
        (1, 30, 22, 14, "Domain 3: Assessment", "#FFF7ED", "#F97316",
         ["Assignment → Questions", "Submission → Marks",
          "QuestionConcept (M:N)", "Release Gating → CMB"]),
        (27, 28, 22, 16, "Domain 4: CMB Engine", "#FAF5FF", "#A855F7",
         ["CMBItem (Bank)", "DiagnosticSession",
          "Response (with confidence)", "CandidateExplanation",
          "Intervention → Resources", "FollowupResult (Verification)"]),
        (1, 7, 48, 10, "Domain 5: Audit & AI Gateway", "#F1F5F9", "#64748B",
         ["AccessLog (Polymorphic)", "AIGatewayRequest → RequestSources",
          "Grounding: lecturer-approved passages sent to LLM"]),
    ]

    for dx, dy, dw, dh, title, bg, border, items in domain_data:
        box = patches.FancyBboxPatch(
            (dx, dy), dw, dh,
            boxstyle="round,pad=0.4,rounding_size=0.6",
            facecolor=bg, edgecolor=border, linewidth=2.0, zorder=2)
        ax.add_patch(box)

        ax.text(dx + 1, dy + dh - 1.5, title,
                fontsize=13, fontweight="bold", color=border, zorder=3)

        for i, item in enumerate(items):
            ax.text(dx + 2, dy + dh - 3.2 - i * 1.6, f"• {item}",
                    fontsize=11, color="#1E293B", zorder=3)

    # Cross-domain arrows
    draw_arrow(ax, 23, 53, 27, 53, "Owns / Enrolls", "#10B981")
    draw_arrow(ax, 12, 47, 12, 44, "Role Gates", "#F97316")
    draw_arrow(ax, 23, 37, 27, 37, "Triggers CMB", "#A855F7")
    draw_arrow(ax, 25, 28, 25, 17, "Audit Logs", "#64748B")

    plt.tight_layout()
    plt.savefig("er_diagram.png", bbox_inches="tight", dpi=200)
    plt.close()
    print("✓ er_diagram.png")


# ─────────────────────────────────────────────
# MASTER SCHEMA OVERVIEW (Dark theme, Large Font)
# ─────────────────────────────────────────────
def gen_schema_overview():
    fig, ax = plt.subplots(figsize=(10, 13), dpi=200)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 65)
    ax.axis("off")
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")

    ax.text(25, 63.5, "LMS Complete Physical Schema Overview",
            ha="center", fontsize=18, fontweight="bold", color="#F8FAFC")
    ax.text(25, 61.5, "27 PostgreSQL Tables across 5 Domains — Column Counts & Key Types",
            ha="center", fontsize=12, color="#94A3B8")

    domain_specs = [
        ("Identity & Access (4 Tables)", "#3B82F6", [
            ("users", "6 cols", "PK: user_id"),
            ("roles", "2 cols", "PK: role_id"),
            ("user_roles", "4 cols", "PK: user_id + role_id"),
            ("lecturer_approval_events", "5 cols", "PK: approval_id"),
        ]),
        ("Courses & Materials (7 Tables)", "#10B981", [
            ("courses", "4 cols", "PK: course_id"),
            ("enrolments", "4 cols", "PK: course_id + user_id"),
            ("concepts", "3 cols", "PK: concept_id"),
            ("concept_prerequisites", "2 cols", "PK: concept_id + prereq"),
            ("materials", "6 cols", "PK: material_id"),
            ("material_sections", "6 cols", "PK: section_id"),
            ("material_section_concepts", "2 cols", "PK: section + concept"),
        ]),
        ("Assessment & Grading (5 Tables)", "#F97316", [
            ("assignments", "8 cols", "PK: assignment_id"),
            ("assignment_questions", "5 cols", "PK: question_id"),
            ("question_concepts", "2 cols", "PK: question + concept"),
            ("submissions", "6 cols", "PK: submission_id"),
            ("marks", "6 cols", "PK: submission + question"),
        ]),
        ("CMB Engine (8 Tables)", "#A855F7", [
            ("cmb_items", "6 cols", "PK: item_id"),
            ("cmb_item_concepts", "2 cols", "PK: item + concept"),
            ("diagnostic_sessions", "4 cols", "PK: session_id"),
            ("responses", "6 cols", "PK: response_id"),
            ("candidate_explanations", "5 cols", "PK: explanation_id"),
            ("interventions", "2 cols", "PK: intervention_id"),
            ("recommended_resources", "3 cols", "PK: intervention + section"),
            ("followup_results", "5 cols", "PK: followup_id"),
        ]),
        ("Audit & AI Gateway (3 Tables)", "#64748B", [
            ("access_logs", "6 cols", "PK: log_id"),
            ("ai_gateway_requests", "7 cols", "PK: request_id"),
            ("ai_gateway_request_sources", "2 cols", "PK: request + section"),
        ]),
    ]

    y = 59
    for domain_title, color, tables in domain_specs:
        ax.text(2, y, domain_title, fontsize=13, fontweight="bold", color=color)
        y -= 1.5
        for tname, cols, pk in tables:
            ax.text(3, y, f"▸ {tname}", fontsize=10.5, fontweight="bold", color="#E2E8F0")
            ax.text(28, y, cols, fontsize=10, color="#94A3B8")
            ax.text(36, y, pk, fontsize=10, color="#CBD5E1")
            y -= 1.5
        y -= 0.8

    plt.tight_layout()
    plt.savefig("complete_schema_diagram.png", bbox_inches="tight", dpi=200)
    plt.close()
    print("✓ complete_schema_diagram.png")


if __name__ == "__main__":
    gen_d1()
    gen_d2()
    gen_d3()
    gen_d4a()
    gen_d4b()
    gen_d5()
    gen_er_overview()
    gen_schema_overview()
    print("\nAll 8 diagrams generated successfully!")
