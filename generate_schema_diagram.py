"""Generate high-resolution Physical Relational Schema Diagram for the LMS Database."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def create_physical_schema_diagram(output_path="complete_schema_diagram.png"):
    fig, ax = plt.subplots(figsize=(20, 13.5), dpi=250)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")

    # Header
    ax.text(
        50,
        98.2,
        "Learning Management System (LMS) - Complete Physical Relational Database Schema Diagram",
        ha="center",
        va="center",
        fontsize=17,
        fontweight="bold",
        color="#F8FAFC",
    )
    ax.text(
        50,
        96.5,
        "PostgreSQL 15+ Physical DDL Blueprint | 27 Tables | Column Types, Nullability, Primary Keys, Foreign Keys & Constraints",
        ha="center",
        va="center",
        fontsize=10.5,
        color="#94A3B8",
    )

    # Palette
    theme = {
        "identity": {"header": "#1E3A8A", "border": "#3B82F6", "bg": "#1E293B", "text": "#F8FAFC"},
        "course": {"header": "#065F46", "border": "#10B981", "bg": "#1E293B", "text": "#F8FAFC"},
        "assessment": {"header": "#9A3412", "border": "#F97316", "bg": "#1E293B", "text": "#F8FAFC"},
        "cmb": {"header": "#581C87", "border": "#A855F7", "bg": "#1E293B", "text": "#F8FAFC"},
        "audit": {"header": "#334155", "border": "#64748B", "bg": "#1E293B", "text": "#F8FAFC"},
    }

    def draw_table_schema(x, y, w, h, table_name, domain_key, columns):
        style = theme[domain_key]
        header_h = 1.7

        # Outer card
        card = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.15,rounding_size=0.35",
            facecolor=style["bg"],
            edgecolor=style["border"],
            linewidth=1.2,
            zorder=3,
        )
        ax.add_patch(card)

        # Header
        hdr = patches.FancyBboxPatch(
            (x, y + h - header_h),
            w,
            header_h,
            boxstyle="round,pad=0.15,rounding_size=0.35",
            facecolor=style["header"],
            edgecolor=style["border"],
            linewidth=1.0,
            zorder=4,
        )
        ax.add_patch(hdr)

        ax.text(
            x + w / 2,
            y + h - header_h / 2,
            table_name,
            ha="center",
            va="center",
            fontsize=11.2,
            fontweight="bold",
            color="#FFFFFF",
            zorder=5,
        )

        spacing = (h - header_h - 0.4) / max(len(columns), 1)
        curr_y = y + h - header_h - 0.45

        for col in columns:
            is_pk = "[PK]" in col
            is_fk = "[FK]" in col

            if is_pk and is_fk:
                badge_color = "#F59E0B"
                txt_color = "#FDE68A"
                weight = "bold"
            elif is_pk:
                badge_color = "#60A5FA"
                txt_color = "#BFDBFE"
                weight = "bold"
            elif is_fk:
                badge_color = "#C084FC"
                txt_color = "#E9D5FF"
                weight = "semibold"
            else:
                badge_color = "#94A3B8"
                txt_color = "#E2E8F0"
                weight = "normal"

            ax.text(
                x + 0.35,
                curr_y,
                col,
                ha="left",
                va="center",
                fontsize=8.6,
                fontweight=weight,
                color=txt_color,
                zorder=5,
            )
            curr_y -= spacing

    # Domain Group Boundary Labels
    group_boxes = [
        (1.5, 66.5, 24.5, 28.0, "Identity & Access Control (4 Tables)", "#1E3A8A"),
        (27.5, 47.0, 32.5, 47.5, "Courses, Materials & Concept Graph (7 Tables)", "#065F46"),
        (61.5, 47.0, 37.0, 47.5, "Assessment & Grading Lifecycle (5 Tables)", "#9A3412"),
        (1.5, 4.0, 58.5, 41.5, "Concept-to-Mastery Bridge (CMB) Engine (8 Tables)", "#581C87"),
        (61.5, 4.0, 37.0, 41.5, "Security Audit Trail & AI Gateway (3 Tables)", "#334155"),
    ]

    for gx, gy, gw, gh, gtitle, gcolor in group_boxes:
        gb = patches.FancyBboxPatch(
            (gx, gy),
            gw,
            gh,
            boxstyle="round,pad=0.25,rounding_size=0.6",
            facecolor="#1E293B",
            edgecolor=gcolor,
            linestyle=":",
            linewidth=1.2,
            alpha=0.6,
            zorder=1,
        )
        ax.add_patch(gb)
        ax.text(
            gx + 1.0,
            gy + gh - 1.2,
            gtitle,
            fontsize=11.0,
            fontweight="bold",
            color=gcolor,
            zorder=2,
        )

    # --- Domain 1: Identity & Access ---
    draw_table_schema(
        2.5,
        79.0,
        11.5,
        13.5,
        "users",
        "identity",
        [
            "[PK] user_id: INT (SERIAL)",
            "username: VARCHAR(50) NULL UQ",
            "email: VARCHAR(255) NOT NULL UQ",
            "password_hash: VARCHAR(255) NOT NULL",
            "account_status: VARCHAR(50) NOT NULL",
            "created_at: TIMESTAMPTZ NOT NULL",
        ],
    )

    draw_table_schema(
        15.0,
        83.5,
        10.0,
        9.0,
        "roles",
        "identity",
        [
            "[PK] role_id: INT (SERIAL)",
            "name: VARCHAR(50) NOT NULL UQ",
            "  CHECK IN ('student', 'lecturer',",
            "            'administrator')",
        ],
    )

    draw_table_schema(
        15.0,
        68.0,
        10.0,
        14.0,
        "user_roles",
        "identity",
        [
            "[PK][FK] user_id: INT (users)",
            "[PK][FK] role_id: INT (roles)",
            "assigned_at: TIMESTAMPTZ NOT NULL",
            "[FK] assigned_by: INT (users)",
            "FK user_id CASCADE",
            "FK role_id CASCADE",
            "FK assigned_by SET NULL",
        ],
    )

    draw_table_schema(
        2.5,
        68.0,
        11.5,
        9.5,
        "lecturer_approval_events",
        "identity",
        [
            "[PK] approval_id: INT (SERIAL)",
            "[FK] lecturer_user_id: INT (users)",
            "[FK] administrator_user_id: INT",
            "decision: VARCHAR(50) NOT NULL",
            "decided_at: TIMESTAMPTZ NOT NULL",
        ],
    )

    # --- Domain 2: Courses & Materials ---
    draw_table_schema(
        29.0,
        79.5,
        14.0,
        12.0,
        "courses",
        "course",
        [
            "[PK] course_id: INT (SERIAL)",
            "title: VARCHAR(255) NOT NULL",
            "[FK] owner_user_id: INT (users)",
            "ai_enabled: BOOLEAN NOT NULL",
            "FK owner_user_id RESTRICT",
        ],
    )

    draw_table_schema(
        44.5,
        81.5,
        14.5,
        10.0,
        "enrolments",
        "course",
        [
            "[PK][FK] course_id: INT (courses)",
            "[PK][FK] user_id: INT (users)",
            "status: VARCHAR(50) NOT NULL",
            "enrolled_at: TIMESTAMPTZ NOT NULL",
            "Composite PK (course_id, user_id)",
        ],
    )

    draw_table_schema(
        29.0,
        64.5,
        14.0,
        13.5,
        "concepts",
        "course",
        [
            "[PK] concept_id: INT (SERIAL)",
            "[FK] course_id: INT (courses)",
            "name: VARCHAR(255) NOT NULL",
            "UQ (course_id, name)",
            "FK course_id CASCADE",
        ],
    )

    draw_table_schema(
        44.5,
        66.5,
        14.5,
        11.5,
        "concept_prerequisites",
        "course",
        [
            "[PK][FK] concept_id: INT (concepts)",
            "[PK][FK] prereq_concept_id: INT",
            "CHECK (concept != prereq)",
            "Composite PK",
            "FK concept_id CASCADE",
            "FK prereq CASCADE",
        ],
    )

    draw_table_schema(
        29.0,
        49.5,
        14.0,
        13.5,
        "materials",
        "course",
        [
            "[PK] material_id: INT (SERIAL)",
            "[FK] course_id: INT (courses)",
            "[FK] uploaded_by: INT (users)",
            "file_path: VARCHAR(512) NOT NULL",
            "processing_status: VARCHAR(50)",
            "uploaded_at: TIMESTAMPTZ NOT NULL",
        ],
    )

    draw_table_schema(
        44.5,
        49.5,
        14.5,
        15.5,
        "material_sections",
        "course",
        [
            "[PK] section_id: INT (SERIAL)",
            "[FK] material_id: INT (materials)",
            "section_order: INT NOT NULL",
            "text: TEXT NOT NULL",
            "source_location_type: VARCHAR(50)",
            "source_location_value: VARCHAR(100)",
            "UQ (material_id, section_order)",
        ],
    )

    draw_table_schema(
        36.5,
        42.0,
        14.5,
        6.5,
        "material_section_concepts",
        "course",
        [
            "[PK][FK] section_id: INT (sections)",
            "[PK][FK] concept_id: INT (concepts)",
            "Composite PK (section_id, concept_id)",
        ],
    )

    # --- Domain 3: Assessment ---
    draw_table_schema(
        63.0,
        77.5,
        16.0,
        15.0,
        "assignments",
        "assessment",
        [
            "[PK] assignment_id: INT (SERIAL)",
            "[FK] course_id: INT (courses)",
            "title: VARCHAR(255) NOT NULL",
            "due_at: TIMESTAMPTZ NOT NULL",
            "lifecycle_status: VARCHAR(50)",
            "results_released_at: TIMESTAMPTZ NULL",
            "[FK] results_released_by: INT NULL",
            "cmb_enabled: BOOLEAN DEFAULT true",
        ],
    )

    draw_table_schema(
        80.5,
        79.0,
        16.5,
        13.5,
        "assignment_questions",
        "assessment",
        [
            "[PK] question_id: INT (SERIAL)",
            "[FK] assignment_id: INT (assignments)",
            "prompt: TEXT NOT NULL",
            "max_score: NUMERIC(5,2) NOT NULL",
            "position: INT NOT NULL",
            "UQ (assignment_id, position)",
        ],
    )

    draw_table_schema(
        63.0,
        59.0,
        16.0,
        15.0,
        "submissions",
        "assessment",
        [
            "[PK] submission_id: INT (SERIAL)",
            "[FK] assignment_id: INT (assignments)",
            "[FK] user_id: INT (users)",
            "submitted_at: TIMESTAMPTZ NOT NULL",
            "work_reference: VARCHAR(512) NOT NULL",
            "marking_status: VARCHAR(50) NOT NULL",
            "UQ (assignment_id, user_id)",
        ],
    )

    draw_table_schema(
        80.5,
        58.5,
        16.5,
        15.5,
        "marks",
        "assessment",
        [
            "[PK][FK] submission_id: INT (subs)",
            "[PK][FK] question_id: INT (questions)",
            "score: NUMERIC(5,2) NOT NULL",
            "lecturer_comment: TEXT NULL",
            "[FK] graded_by: INT (users) RESTRICT",
            "graded_at: TIMESTAMPTZ NOT NULL",
            "Composite PK (sub_id, q_id)",
        ],
    )

    draw_table_schema(
        80.5,
        49.5,
        16.5,
        7.5,
        "question_concepts",
        "assessment",
        [
            "[PK][FK] question_id: INT (questions)",
            "[PK][FK] concept_id: INT (concepts)",
            "Composite PK (question_id, concept_id)",
        ],
    )

    # --- Domain 4: CMB ---
    draw_table_schema(
        2.5,
        27.0,
        13.0,
        15.5,
        "cmb_items",
        "cmb",
        [
            "[PK] item_id: INT (SERIAL)",
            "[FK] course_id: INT (courses)",
            "item_type: VARCHAR(50) NOT NULL",
            "  CHECK IN ('diagnostic', 'practice',",
            "            'verification')",
            "prompt: TEXT NOT NULL",
            "review_status: VARCHAR(50) NOT NULL",
            "[FK] approved_by: INT NULL",
        ],
    )

    draw_table_schema(
        16.5,
        34.0,
        11.5,
        8.0,
        "cmb_item_concepts",
        "cmb",
        [
            "[PK][FK] item_id: INT (cmb_items)",
            "[PK][FK] concept_id: INT (concepts)",
            "Composite PK (item_id, concept_id)",
        ],
    )

    draw_table_schema(
        29.0,
        27.0,
        13.5,
        12.5,
        "diagnostic_sessions",
        "cmb",
        [
            "[PK] session_id: INT (SERIAL)",
            "[FK] submission_id: INT (submissions)",
            "started_at: TIMESTAMPTZ NOT NULL",
            "completed_at: TIMESTAMPTZ NULL",
            "FK submission_id CASCADE",
        ],
    )

    draw_table_schema(
        43.5,
        25.5,
        15.0,
        16.0,
        "responses",
        "cmb",
        [
            "[PK] response_id: INT (SERIAL)",
            "[FK] session_id: INT (sessions)",
            "[FK] item_id: INT (cmb_items)",
            "answer: TEXT NOT NULL",
            "confidence_choice: VARCHAR(50) NULL",
            "response_time: INT NULL",
            "FK session_id CASCADE",
            "FK item_id RESTRICT",
        ],
    )

    draw_table_schema(
        2.5,
        6.5,
        13.5,
        16.0,
        "candidate_explanations",
        "cmb",
        [
            "[PK] explanation_id: INT (SERIAL)",
            "[FK] session_id: INT (sessions)",
            "[FK] concept_id: INT (concepts)",
            "label: VARCHAR(255) NOT NULL",
            "confidence: FLOAT NOT NULL",
            "FK session_id CASCADE",
            "FK concept_id CASCADE",
        ],
    )

    draw_table_schema(
        17.0,
        8.0,
        12.0,
        11.5,
        "interventions",
        "cmb",
        [
            "[PK] intervention_id: INT (SERIAL)",
            "[FK] explanation_id: INT (explanations)",
            "FK explanation_id CASCADE",
        ],
    )

    draw_table_schema(
        30.0,
        6.5,
        14.0,
        14.5,
        "recommended_resources",
        "cmb",
        [
            "[PK][FK] intervention_id: INT (interv)",
            "[PK][FK] section_id: INT (sections)",
            "reason: TEXT NULL",
            "Composite PK",
            "FK intervention_id CASCADE",
            "FK section_id CASCADE",
        ],
    )

    draw_table_schema(
        45.0,
        6.5,
        13.5,
        14.5,
        "followup_results",
        "cmb",
        [
            "[PK] followup_id: INT (SERIAL)",
            "[FK] intervention_id: INT (interv)",
            "[FK] item_id: INT (cmb_items verif)",
            "correct: BOOLEAN NOT NULL",
            "answered_at: TIMESTAMPTZ NOT NULL",
            "FK item_id RESTRICT",
        ],
    )

    # --- Domain 5: Audit & Gateway ---
    draw_table_schema(
        63.0,
        24.0,
        16.0,
        17.0,
        "access_logs",
        "audit",
        [
            "[PK] log_id: INT (SERIAL)",
            "[FK] user_id: INT NULL (users)",
            "action: VARCHAR(100) NOT NULL",
            "target_type: VARCHAR(100) NOT NULL",
            "target_id: VARCHAR(100) NOT NULL",
            "occurred_at: TIMESTAMPTZ NOT NULL",
            "FK user_id ON DELETE SET NULL",
            "Polymorphic target reference",
        ],
    )

    draw_table_schema(
        80.5,
        24.0,
        16.5,
        17.0,
        "ai_gateway_requests",
        "audit",
        [
            "[PK] request_id: INT (SERIAL)",
            "[FK] user_id: INT (users)",
            "[FK] course_id: INT (courses)",
            "purpose: VARCHAR(100) NOT NULL",
            "provider: VARCHAR(100) NOT NULL",
            "status: VARCHAR(50) NOT NULL",
            "created_at: TIMESTAMPTZ NOT NULL",
        ],
    )

    draw_table_schema(
        80.5,
        6.5,
        16.5,
        13.5,
        "ai_gateway_request_sources",
        "audit",
        [
            "[PK][FK] request_id: INT (ai_req)",
            "[PK][FK] section_id: INT (sections)",
            "Composite PK",
            "FK request_id CASCADE",
            "FK section_id CASCADE",
            "Grounding citations sent to AI",
        ],
    )

    # Connectors
    def connect(p1, p2, color="#60A5FA"):
        ax.annotate(
            "",
            xy=p2,
            xytext=p1,
            arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2, mutation_scale=9),
            zorder=6,
        )

    connect((14.0, 85.0), (15.0, 75.0), "#60A5FA")
    connect((14.0, 87.0), (29.0, 87.0), "#10B981")
    connect((43.0, 85.0), (44.5, 85.0), "#10B981")
    connect((36.0, 79.5), (36.0, 78.0), "#10B981")
    connect((36.0, 64.5), (36.0, 63.0), "#10B981")
    connect((43.0, 56.5), (44.5, 56.5), "#10B981")
    connect((43.0, 83.5), (63.0, 83.5), "#F97316")
    connect((79.0, 85.0), (80.5, 85.0), "#F97316")
    connect((71.0, 77.5), (71.0, 74.0), "#F97316")
    connect((79.0, 66.5), (80.5, 66.5), "#F97316")
    connect((63.0, 63.0), (35.0, 39.5), "#A855F7")
    connect((36.0, 27.0), (43.5, 27.0), "#A855F7")
    connect((35.0, 27.0), (16.0, 16.5), "#A855F7")
    connect((16.0, 12.0), (17.0, 12.0), "#A855F7")
    connect((29.0, 12.0), (30.0, 12.0), "#A855F7")
    connect((29.0, 9.5), (45.0, 9.5), "#A855F7")
    connect((88.5, 24.0), (88.5, 20.0), "#94A3B8")

    ax.text(
        63.0,
        1.5,
        "SCHEMA SPECIFICATION: 27 Normalized Entities | PostgreSQL 15+ Dialect | Generated via SQLAlchemy 2.0 ORM & Alembic",
        fontsize=8.5,
        fontweight="bold",
        color="#94A3B8",
    )

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Physical schema diagram saved to {output_path} successfully!")


if __name__ == "__main__":
    create_physical_schema_diagram("complete_schema_diagram.png")
