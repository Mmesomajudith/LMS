"""Generate high-resolution Conceptual / Logical Entity-Relationship (ER) Diagram for LMS."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def create_conceptual_er_diagram(output_path="er_diagram.png"):
    fig, ax = plt.subplots(figsize=(19, 12.5), dpi=250)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    # Banner
    ax.text(
        50,
        98.2,
        "Learning Management System (LMS) - Logical Entity-Relationship (ER) Diagram",
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#0F172A",
    )
    ax.text(
        50,
        96.2,
        "Conceptual & Logical Entity Cardinality Model | 5 Core Domains | Concept-to-Mastery Bridge (CMB) Workflow",
        ha="center",
        va="center",
        fontsize=11,
        color="#475569",
    )

    # Domain Containers
    domains = [
        # (x, y, w, h, title, bg_color, border_color)
        (2.0, 68.0, 24.0, 26.0, "Domain 1: Identity & Access Control", "#EFF6FF", "#3B82F6"),
        (28.5, 48.0, 32.0, 46.0, "Domain 2: Courses, Prerequisite Map & Materials", "#ECFDF5", "#10B981"),
        (63.0, 48.0, 35.0, 46.0, "Domain 3: Assessment & Student Work Lifecycle", "#FFF7ED", "#F97316"),
        (2.0, 4.0, 58.5, 41.5, "Domain 4: Concept-to-Mastery Bridge (CMB Engine)", "#FAF5FF", "#A855F7"),
        (63.0, 4.0, 35.0, 41.5, "Domain 5: Security Audit Trail & AI Gateway", "#F1F5F9", "#64748B"),
    ]

    for rx, ry, rw, rh, rtitle, rbg, rborder in domains:
        box = patches.FancyBboxPatch(
            (rx, ry),
            rw,
            rh,
            boxstyle="round,pad=0.3,rounding_size=0.8",
            facecolor=rbg,
            edgecolor=rborder,
            linestyle="--",
            linewidth=1.3,
            alpha=0.55,
            zorder=1,
        )
        ax.add_patch(box)
        ax.text(
            rx + 1.2,
            ry + rh - 1.2,
            rtitle,
            fontsize=11.5,
            fontweight="bold",
            color="#1E293B",
            zorder=2,
        )

    # Entity Box Drawer
    def draw_entity(x, y, w, h, name, key_attrs, rel_summary, header_color):
        rect = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.2,rounding_size=0.4",
            facecolor="#FFFFFF",
            edgecolor=header_color,
            linewidth=1.4,
            zorder=3,
        )
        ax.add_patch(rect)

        header_h = 1.6
        header = patches.FancyBboxPatch(
            (x, y + h - header_h),
            w,
            header_h,
            boxstyle="round,pad=0.2,rounding_size=0.4",
            facecolor=header_color,
            edgecolor=header_color,
            linewidth=1.2,
            zorder=4,
        )
        ax.add_patch(header)

        ax.text(
            x + w / 2,
            y + h - header_h / 2,
            name,
            ha="center",
            va="center",
            fontsize=11.5,
            fontweight="bold",
            color="#FFFFFF",
            zorder=5,
        )

        curr_y = y + h - header_h - 0.5
        spacing = (h - header_h - 0.4) / max(len(key_attrs) + len(rel_summary) + 1, 1)

        ax.text(x + 0.35, curr_y, "Key Attributes:", fontsize=9.2, fontweight="bold", color="#334155", zorder=5)
        curr_y -= spacing

        for attr in key_attrs:
            color = "#1D4ED8" if "[PK]" in attr else ("#B45309" if "[FK]" in attr else "#0F172A")
            ax.text(x + 0.45, curr_y, f"• {attr}", fontsize=8.5, color=color, zorder=5)
            curr_y -= spacing

        ax.text(x + 0.35, curr_y, "Relationships:", fontsize=9.2, fontweight="bold", color="#334155", zorder=5)
        curr_y -= spacing

        for rel in rel_summary:
            ax.text(x + 0.45, curr_y, f"→ {rel}", fontsize=8.2, color="#475569", zorder=5)
            curr_y -= spacing

    # --- Domain 1 Entities ---
    draw_entity(
        3.2,
        80.5,
        10.5,
        11.5,
        "User (Entity)",
        ["[PK] user_id", "email (UQ)", "username (UQ)", "account_status"],
        ["M:N to Role (user_roles)", "1:N Courses owned", "1:N Submissions"],
        "#1E3A8A",
    )

    draw_entity(
        15.0,
        83.0,
        9.5,
        9.0,
        "Role (Entity)",
        ["[PK] role_id", "name (UQ)"],
        ["M:N to User", "Roles: student, lecturer, admin"],
        "#1E3A8A",
    )

    draw_entity(
        15.0,
        70.0,
        9.5,
        11.0,
        "UserRole (Junction)",
        ["[PK][FK] user_id", "[PK][FK] role_id", "assigned_at", "[FK] assigned_by"],
        ["Links User to Role", "Audit assigner (Admin)"],
        "#2563EB",
    )

    draw_entity(
        3.2,
        70.0,
        10.5,
        9.0,
        "LecturerApprovalEvent",
        ["[PK] approval_id", "[FK] lecturer_user_id", "[FK] admin_user_id", "decision, decided_at"],
        ["Admin approves lecturer", "Preserves approval audit"],
        "#1E3A8A",
    )

    # --- Domain 2 Entities ---
    draw_entity(
        30.0,
        79.0,
        13.0,
        11.5,
        "Course (Entity)",
        ["[PK] course_id", "title", "[FK] owner_user_id", "ai_enabled"],
        ["1:N Concepts", "1:N Materials", "1:N Assignments", "M:N Users (Enrolments)"],
        "#065F46",
    )

    draw_entity(
        45.0,
        81.5,
        14.0,
        9.0,
        "Enrolment (Junction)",
        ["[PK][FK] course_id", "[PK][FK] user_id", "status, enrolled_at"],
        ["M:N Course to Student", "Statuses: enrolled, completed"],
        "#059669",
    )

    draw_entity(
        30.0,
        64.5,
        13.0,
        11.5,
        "Concept (Entity)",
        ["[PK] concept_id", "[FK] course_id", "name (UQ/course)"],
        ["Directed graph (Prereqs)", "Mapped to Sections", "Mapped to Questions & CMB"],
        "#065F46",
    )

    draw_entity(
        45.0,
        66.5,
        14.0,
        9.5,
        "ConceptPrerequisite",
        ["[PK][FK] concept_id", "[PK][FK] prereq_concept_id"],
        ["Directed prerequisite edge", "Check: self-prereq blocked"],
        "#059669",
    )

    draw_entity(
        30.0,
        50.5,
        13.0,
        11.5,
        "Material (Entity)",
        ["[PK] material_id", "[FK] course_id", "[FK] uploaded_by", "file_path, status"],
        ["1:N MaterialSections", "Uploaded by Lecturer"],
        "#065F46",
    )

    draw_entity(
        45.0,
        50.0,
        14.0,
        13.5,
        "MaterialSection (Entity)",
        ["[PK] section_id", "[FK] material_id", "section_order (UQ)", "text, location_type/val"],
        ["Citable passage / slide", "M:N Concepts (SectionConcept)", "Grounding for AI Gateway"],
        "#065F46",
    )

    # --- Domain 3 Entities ---
    draw_entity(
        64.5,
        78.0,
        14.5,
        13.5,
        "Assignment (Entity)",
        ["[PK] assignment_id", "[FK] course_id", "title, due_at", "results_released_at/by", "cmb_enabled"],
        ["1:N Questions", "1:N Submissions", "Release Gating for CMB"],
        "#9A3412",
    )

    draw_entity(
        81.0,
        79.0,
        15.5,
        12.5,
        "AssignmentQuestion (Entity)",
        ["[PK] question_id", "[FK] assignment_id", "prompt, max_score", "position (UQ/asgn)"],
        ["Belongs to Assignment", "M:N Concepts", "1:N Marks per submission"],
        "#9A3412",
    )

    draw_entity(
        64.5,
        59.0,
        14.5,
        13.5,
        "Submission (Entity)",
        ["[PK] submission_id", "[FK] assignment_id", "[FK] user_id", "work_reference, status"],
        ["Submitted by Student", "UQ(asgn_id, user_id)", "1:N Marks", "1:N DiagnosticSessions"],
        "#9A3412",
    )

    draw_entity(
        81.0,
        58.5,
        15.5,
        14.0,
        "Mark (Entity)",
        ["[PK][FK] submission_id", "[PK][FK] question_id", "score, lecturer_comment", "[FK] graded_by, graded_at"],
        ["Question score & comment", "Graded by Lecturer", "Triggers CMB lost-mark detection"],
        "#C2410C",
    )

    # --- Domain 4 Entities ---
    draw_entity(
        3.5,
        27.0,
        13.0,
        14.5,
        "CMBItem (Bank Entity)",
        ["[PK] item_id", "[FK] course_id", "item_type (Check)", "prompt, review_status", "[FK] approved_by"],
        ["Types: diag, practice, verif", "M:N Concepts", "Answered in Sessions & Followups"],
        "#581C87",
    )

    draw_entity(
        18.0,
        28.0,
        12.5,
        12.5,
        "DiagnosticSession (Entity)",
        ["[PK] session_id", "[FK] submission_id", "started_at, completed_at"],
        ["Triggered on released results", "1:N Responses", "1:N CandidateExplanations"],
        "#581C87",
    )

    draw_entity(
        32.0,
        26.5,
        13.0,
        15.0,
        "Response (Entity)",
        ["[PK] response_id", "[FK] session_id", "[FK] item_id", "answer, confidence_choice", "response_time"],
        ["Student diagnostic attempt", "Captures metacognitive confidence", "Informs gap reasoning"],
        "#6B21A8",
    )

    draw_entity(
        3.5,
        6.5,
        13.0,
        15.0,
        "CandidateExplanation",
        ["[PK] explanation_id", "[FK] session_id", "[FK] concept_id", "label, confidence"],
        ["Misconception hypothesis", "Probabilistic (0.0 - 1.0)", "1:N Interventions"],
        "#581C87",
    )

    draw_entity(
        18.0,
        8.0,
        11.5,
        11.0,
        "Intervention (Entity)",
        ["[PK] intervention_id", "[FK] explanation_id"],
        ["Targeted remediation plan", "Links to RecommendedResources", "1:N FollowupResults"],
        "#581C87",
    )

    draw_entity(
        31.0,
        6.5,
        13.5,
        14.0,
        "RecommendedResource",
        ["[PK][FK] intervention_id", "[PK][FK] section_id", "reason"],
        ["Links to MaterialSection", "Lecturer-authored passage", "Clear pedagogical reason"],
        "#7E22CE",
    )

    draw_entity(
        46.0,
        6.5,
        13.0,
        14.0,
        "FollowupResult (Entity)",
        ["[PK] followup_id", "[FK] intervention_id", "[FK] item_id (verif)", "correct, answered_at"],
        ["Verifies learning change", "Uses fresh verification item", "Never original assignment task"],
        "#581C87",
    )

    # --- Domain 5 Entities ---
    draw_entity(
        64.5,
        25.0,
        14.5,
        15.5,
        "AccessLog (Audit Entity)",
        ["[PK] log_id", "[FK] user_id (SET NULL)", "action, target_type", "target_id, occurred_at"],
        ["Polymorphic security audit", "Logs release events & views", "Preserved on user deletion"],
        "#334155",
    )

    draw_entity(
        81.0,
        24.0,
        15.5,
        16.5,
        "AIGatewayRequest (Audit)",
        ["[PK] request_id", "[FK] user_id", "[FK] course_id", "purpose, provider, status", "created_at"],
        ["External LLM tracking", "Enforces course.ai_enabled", "Links to request sources"],
        "#334155",
    )

    draw_entity(
        81.0,
        6.5,
        15.5,
        12.0,
        "AIGatewayRequestSource",
        ["[PK][FK] request_id", "[PK][FK] section_id"],
        ["Captures grounding passages", "Ensures reproducibility", "Zero prompt leakage"],
        "#475569",
    )

    # Conceptual Relationship Connectors
    def connect(p1, p2, color="#475569", label=None, label_pos=None):
        ax.annotate(
            "",
            xy=p2,
            xytext=p1,
            arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3, mutation_scale=10),
            zorder=6,
        )
        if label and label_pos:
            ax.text(
                label_pos[0],
                label_pos[1],
                label,
                fontsize=7.0,
                fontweight="bold",
                color=color,
                bbox=dict(boxstyle="square,pad=0.15", facecolor="#FFFFFF", edgecolor="none", alpha=0.85),
                zorder=7,
            )

    connect((13.7, 85.0), (15.0, 75.0), "#3B82F6", "1:N", (13.8, 80.0))
    connect((19.5, 83.0), (19.5, 81.0), "#3B82F6", "1:N", (19.7, 82.0))
    connect((13.7, 86.5), (30.0, 86.5), "#10B981", "1:N (Owns)", (21.5, 87.0))
    connect((43.0, 85.0), (45.0, 85.0), "#10B981", "1:N", (43.5, 85.5))
    connect((36.5, 79.0), (36.5, 76.0), "#10B981", "1:N", (36.8, 77.5))
    connect((36.5, 64.5), (36.5, 62.0), "#10B981", "1:N", (36.8, 63.2))
    connect((43.0, 56.0), (45.0, 56.0), "#10B981", "1:N", (43.5, 56.5))
    connect((43.0, 84.0), (64.5, 84.0), "#F97316", "1:N", (53.5, 84.5))
    connect((79.0, 85.0), (81.0, 85.0), "#F97316", "1:N", (79.5, 85.5))
    connect((71.5, 78.0), (71.5, 72.5), "#F97316", "1:N", (72.0, 75.0))
    connect((79.0, 65.5), (81.0, 65.5), "#F97316", "1:1", (79.5, 66.2))
    connect((64.5, 63.0), (25.0, 40.5), "#A855F7", "CMB Gated (1:N)", (42.0, 52.0))
    connect((24.0, 34.0), (32.0, 34.0), "#A855F7", "1:N", (27.5, 34.5))
    connect((24.0, 28.0), (10.0, 21.5), "#A855F7", "1:N", (16.5, 24.5))
    connect((10.0, 6.5), (18.0, 13.0), "#A855F7", "1:N", (13.5, 9.5))
    connect((29.5, 13.5), (31.0, 13.5), "#A855F7", "1:N", (29.8, 14.2))
    connect((29.5, 10.0), (46.0, 10.0), "#A855F7", "1:N", (37.5, 10.5))
    connect((88.5, 24.0), (88.5, 18.5), "#64748B", "1:N", (89.0, 21.0))

    ax.text(
        64.5,
        1.5,
        "Cardinality Legend:  1:1 One-to-One | 1:N One-to-Many | M:N Many-to-Many | [PK] Primary Key | [FK] Foreign Key | (UQ) Unique Constraint",
        fontsize=8.5,
        fontweight="bold",
        color="#334155",
    )

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Conceptual ER diagram saved to {output_path} successfully!")


if __name__ == "__main__":
    create_conceptual_er_diagram("er_diagram.png")
