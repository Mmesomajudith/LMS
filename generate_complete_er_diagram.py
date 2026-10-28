"""Generate an exhaustive Entity-Relationship diagram for the 27-table LMS schema."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUTPUT = "complete_er_diagram.png"

TABLES = {
    "users": (["PK user_id", "email UQ", "password_hash", "account_status", "created_at"], (0, 5.15), "identity"),
    "roles": (["PK role_id", "name UQ"], (4.2, 5.15), "identity"),
    "user_roles": (["PK/FK user_id", "PK/FK role_id", "assigned_at", "FK assigned_by"], (8.4, 5.15), "identity"),
    "lecturer_approval_events": (["PK approval_id", "FK lecturer_user_id", "FK administrator_user_id", "decision", "decided_at"], (12.6, 5.15), "identity"),

    "courses": (["PK course_id", "title", "FK owner_user_id", "ai_enabled"], (0, 9.7), "course"),
    "enrolments": (["PK/FK course_id", "PK/FK user_id", "status", "enrolled_at"], (4.2, 9.7), "course"),
    "concepts": (["PK concept_id", "FK course_id", "name"], (8.4, 9.7), "course"),
    "concept_prerequisites": (["PK/FK concept_id", "PK/FK prereq_concept_id"], (12.6, 9.7), "course"),
    "materials": (["PK material_id", "FK course_id", "FK uploaded_by", "file_path", "status"], (16.8, 9.7), "course"),
    "material_sections": (["PK section_id", "FK material_id", "order", "text", "source location"], (21.0, 9.7), "course"),
    "material_section_concepts": (["PK/FK section_id", "PK/FK concept_id"], (25.2, 9.7), "course"),

    "assignments": (["PK assignment_id", "FK course_id", "title", "due_at", "release fields", "cmb_enabled"], (0, 14.25), "assessment"),
    "assignment_questions": (["PK question_id", "FK assignment_id", "prompt", "max_score", "position"], (4.2, 14.25), "assessment"),
    "question_concepts": (["PK/FK question_id", "PK/FK concept_id"], (8.4, 14.25), "assessment"),
    "submissions": (["PK submission_id", "FK assignment_id", "FK user_id", "work", "marking_status"], (12.6, 14.25), "assessment"),
    "marks": (["PK/FK submission_id", "PK/FK question_id", "score", "comment", "FK graded_by"], (16.8, 14.25), "assessment"),

    "cmb_items": (["PK item_id", "FK course_id", "item_type", "prompt", "review_status", "FK approved_by"], (0, 18.8), "cmb"),
    "cmb_item_concepts": (["PK/FK item_id", "PK/FK concept_id"], (4.2, 18.8), "cmb"),
    "diagnostic_sessions": (["PK session_id", "FK submission_id", "started_at", "completed_at"], (8.4, 18.8), "cmb"),
    "responses": (["PK response_id", "FK session_id", "FK item_id", "answer", "confidence", "time"], (12.6, 18.8), "cmb"),
    "candidate_explanations": (["PK explanation_id", "FK session_id", "FK concept_id", "label", "confidence"], (16.8, 18.8), "cmb"),
    "interventions": (["PK intervention_id", "FK explanation_id"], (21.0, 18.8), "cmb"),
    "recommended_resources": (["PK/FK intervention_id", "PK/FK section_id", "reason"], (25.2, 18.8), "cmb"),
    "followup_results": (["PK followup_id", "FK intervention_id", "FK item_id", "correct", "answered_at"], (29.4, 18.8), "cmb"),

    "access_logs": (["PK log_id", "FK user_id", "action", "target_type/id", "occurred_at"], (0, 23.35), "audit"),
    "ai_gateway_requests": (["PK request_id", "FK user_id", "FK course_id", "purpose", "provider", "status"], (4.2, 23.35), "audit"),
    "ai_gateway_request_sources": (["PK/FK request_id", "PK/FK section_id"], (8.4, 23.35), "audit"),
}

RELATIONS = [
    ("roles", "user_roles"), ("users", "user_roles"), ("users", "user_roles"),
    ("users", "lecturer_approval_events"), ("users", "lecturer_approval_events"),
    ("users", "courses"), ("courses", "enrolments"), ("users", "enrolments"),
    ("courses", "concepts"), ("concepts", "concept_prerequisites"), ("concepts", "concept_prerequisites"),
    ("courses", "materials"), ("users", "materials"), ("materials", "material_sections"),
    ("material_sections", "material_section_concepts"), ("concepts", "material_section_concepts"),
    ("courses", "assignments"), ("users", "assignments"), ("assignments", "assignment_questions"),
    ("assignment_questions", "question_concepts"), ("concepts", "question_concepts"),
    ("assignments", "submissions"), ("users", "submissions"),
    ("submissions", "marks"), ("assignment_questions", "marks"), ("users", "marks"),
    ("courses", "cmb_items"), ("users", "cmb_items"), ("cmb_items", "cmb_item_concepts"), ("concepts", "cmb_item_concepts"),
    ("submissions", "diagnostic_sessions"), ("diagnostic_sessions", "responses"), ("cmb_items", "responses"),
    ("diagnostic_sessions", "candidate_explanations"), ("concepts", "candidate_explanations"),
    ("candidate_explanations", "interventions"), ("interventions", "recommended_resources"),
    ("material_sections", "recommended_resources"), ("interventions", "followup_results"), ("cmb_items", "followup_results"),
    ("users", "access_logs"), ("users", "ai_gateway_requests"), ("courses", "ai_gateway_requests"),
    ("ai_gateway_requests", "ai_gateway_request_sources"), ("material_sections", "ai_gateway_request_sources"),
]

COLORS = {
    "identity": ("#1E3A8A", "#3B82F6"),
    "course": ("#065F46", "#10B981"),
    "assessment": ("#9A3412", "#F97316"),
    "cmb": ("#581C87", "#A855F7"),
    "audit": ("#334155", "#64748B"),
}


def draw_box(ax, name, columns, center, domain):
    header_color, border_color = COLORS[domain]
    x, y = center
    w, h = 3.7, 3.25
    if name == "lecturer_approval_events" or name == "material_section_concepts" or name == "ai_gateway_request_sources":
        w = 3.9
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                         facecolor="#FFFFFF", edgecolor=border_color, linewidth=1.5, zorder=4)
    ax.add_patch(box)
    ax.add_patch(FancyBboxPatch((x, y + h - 0.7), w, 0.7, boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor=header_color, edgecolor=header_color, linewidth=0, zorder=5))
    ax.text(x + w / 2, y + h - 0.35, name, ha="center", va="center", fontsize=9,
            fontweight="bold", color="white", zorder=6)
    for index, column in enumerate(columns):
        cy = y + h - 0.95 - index * 0.42
        color = "#B45309" if column.startswith("PK/FK") else ("#1D4ED8" if column.startswith("PK") else "#1E293B")
        ax.text(x + 0.18, cy, "• " + column, ha="left", va="center", fontsize=7,
                color=color, zorder=6)
    return (x, y, w, h)


def center(rect):
    x, y, w, h = rect
    return (x + w / 2, y + h / 2)


def main():
    fig, ax = plt.subplots(figsize=(34, 26), dpi=220)
    ax.set_xlim(-1, 34)
    ax.set_ylim(2.0, 27.5)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(16.5, 26.8,
            "Learning Management System — Complete Entity-Relationship Diagram",
            ha="center", fontsize=22, fontweight="bold", color="#0F172A")
    ax.text(16.5, 26.1,
            "All 27 physical tables and every documented foreign-key relationship",
            ha="center", fontsize=12, color="#475569")

    sections = [
        (4.15, "Identity & Access — 4 tables", "#1E3A8A", 3.9, 4.55, 13.8, 4.35),
        (0.0, "Courses & Materials — 7 tables", "#065F46", -1, 8.0, 29.9, 6.25),
        (0.0, "Assessment — 5 tables", "#9A3412", -1, 13.0, 21.0, 5.0),
        (0.0, "Concept-to-Mastery Bridge — 8 tables", "#581C87", -1, 17.55, 33.6, 5.3),
        (0.0, "Audit & AI Gateway — 3 tables", "#334155", -1, 22.1, 13.0, 5.0),
    ]
    for x, title, color, bx, by, bw, bh in sections:
        if x != 4.15:
            box = FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.2,rounding_size=0.2",
                                 facecolor="#FFFFFF", edgecolor=color, linewidth=1.5, linestyle="--", alpha=0.48, zorder=1)
            ax.add_patch(box)
            ax.text(bx + 0.35, by + bh - 0.42, title, fontsize=11, fontweight="bold", color=color, zorder=2)
        else:
            ax.text(16.5, 4.55, title, fontsize=11, fontweight="bold", color=color, ha="center")

    rects = {}
    for name, (columns, pos, domain) in TABLES.items():
        rects[name] = draw_box(ax, name, columns, pos, domain)

    centers = {name: center(rect) for name, rect in rects.items()}

    for source, target in RELATIONS:
        x1, y1 = centers[source]
        x2, y2 = centers[target]
        arrow = FancyArrowPatch((x1, y1), (x2, y2), connectionstyle="arc3,rad=0.02",
                                arrowstyle="-|>", mutation_scale=8, linewidth=0.75,
                                color="#64748B", alpha=0.68, zorder=3)
        ax.add_patch(arrow)

    ax.text(16.5, 2.7,
            "Legend: PK = primary key  |  FK = foreign key  |  PK/FK = junction-table key  |  UQ = unique  |  Arrow = foreign-key relationship",
            ha="center", fontsize=9.5, color="#334155")

    plt.tight_layout()
    plt.savefig(OUTPUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(OUTPUT)


if __name__ == "__main__":
    main()
