"""Generate detailed ER documentation directly from the live PostgreSQL database."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from sqlalchemy import inspect
from app.database import engine

OUTPUT_STEM = "LIVE_POSTGRES_ER_DIAGRAM"

DOMAIN = {
    "identity": {"tables": ["faculties", "departments", "users", "roles", "user_roles", "lecturer_approval_events"], "title": "Identity, Faculty & Department", "color": "#1E3A8A", "border": "#3B82F6"},
    "course": {"tables": ["courses", "enrolments", "concepts", "concept_prerequisites", "materials", "material_sections", "material_section_concepts"], "title": "Courses & Materials", "color": "#065F46", "border": "#10B981"},
    "assessment": {"tables": ["assignments", "assignment_questions", "question_concepts", "submissions", "marks"], "title": "Assessment & Grading", "color": "#9A3412", "border": "#F97316"},
    "cmb": {"tables": ["cmb_items", "cmb_item_concepts", "diagnostic_sessions", "responses", "candidate_explanations", "interventions", "recommended_resources", "followup_results"], "title": "Concept-to-Mastery Bridge", "color": "#581C87", "border": "#A855F7"},
    "audit": {"tables": ["access_logs", "ai_gateway_requests", "ai_gateway_request_sources"], "title": "Audit & AI Gateway", "color": "#334155", "border": "#64748B"},
}


def main():
    inspector = inspect(engine)
    table_names = [t for t in inspector.get_table_names() if t != "alembic_version"]

    fig, ax = plt.subplots(figsize=(38, 26), dpi=180)
    ax.set_xlim(-2, 64)
    ax.set_ylim(-3, 30)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    ax.text(31, 28.8, "LMS Live PostgreSQL Entity-Relationship Diagram",
            ha="center", fontsize=24, fontweight="bold", color="#0F172A")
    ax.text(31, 27.9,
            "Generated directly from live PostgreSQL metadata • PK, FK, unique constraints and column types",
            ha="center", fontsize=11, color="#475569")

    positions = {}
    widths = {"identity": 12, "course": 12, "assessment": 12, "cmb": 12, "audit": 12}
    x_starts = {"identity": -1, "course": 12.0, "assessment": 25.0, "cmb": 38.0, "audit": 51.0}

    for domain_name, domain in DOMAIN.items():
        x = x_starts[domain_name]
        ax.text(x, 26.9, domain["title"], fontsize=12, fontweight="bold", color=domain["color"])
        ax.plot([x, x + widths[domain_name] - 0.2], [26.5, 26.5], color=domain["border"], lw=2)
        for row, table in enumerate(domain["tables"]):
            if table not in table_names:
                continue
            y = 25.7 - row * 4.15
            rect_h = draw_table(ax, x, y, widths[domain_name] - 0.4, table, inspector, domain)
            positions[table] = (x + (widths[domain_name] - 0.4) / 2, y + rect_h / 2)

    for table in table_names:
        if table in positions:
            for fk in inspector.get_foreign_keys(table):
                target = fk["referred_table"]
                if target in positions:
                    x1, y1 = positions[table]
                    x2, y2 = positions[target]
                    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                                 connectionstyle="arc3,rad=0.08",
                                                 arrowstyle="-|>", mutation_scale=8,
                                                 linewidth=0.75, color="#64748B", alpha=0.72,
                                                 zorder=2))

    ax.text(31, -1.8,
            "Legend: [PK] primary key • [FK] foreign key • [UQ] unique constraint • arrows point to referenced tables",
            ha="center", fontsize=9, color="#334155")

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_STEM}.png", bbox_inches="tight", dpi=220)
    plt.savefig(f"{OUTPUT_STEM}.svg", bbox_inches="tight")
    plt.savefig(f"{OUTPUT_STEM}.pdf", bbox_inches="tight")
    plt.close()

    # Machine-readable relationship inventory matching the live database.
    lines = [
        "# Live PostgreSQL ER Diagram Inventory",
        "",
        "Generated directly from the configured PostgreSQL database.",
        "",
        "## Tables",
    ]
    for table in table_names:
        pk = inspector.get_pk_constraint(table).get("constrained_columns", [])
        unique = [u["column_names"] for u in inspector.get_unique_constraints(table)]
        fk_rows = inspector.get_foreign_keys(table)
        lines.append(f"### `{table}`")
        lines.append("")
        lines.append("| Column | PostgreSQL type | Null | Key |")
        lines.append("|---|---|---:|---|")
        for column in inspector.get_columns(table):
            name = column["name"]
            key = []
            if name in pk: key.append("PK")
            if any(name in fk["constrained_columns"] for fk in fk_rows): key.append("FK")
            if any(name in names for names in unique): key.append("UQ")
            lines.append(f"| `{name}` | `{column['type']}` | {'NULL' if column['nullable'] else 'NOT NULL'} | {' + '.join(key) or '—'} |")
        if fk_rows:
            lines.append("")
            lines.append("Foreign keys:")
            for fk in fk_rows:
                lines.append(f"- `{', '.join(fk['constrained_columns'])}` → `{fk['referred_table']}` (`{', '.join(fk['referred_columns'])}`)")
        lines.append("")
    with open(f"{OUTPUT_STEM}_INVENTORY.md", "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def draw_table(ax, x, y, width, table, inspector, domain):
    columns = inspector.get_columns(table)
    pk = inspector.get_pk_constraint(table).get("constrained_columns", [])
    fks = inspector.get_foreign_keys(table)
    fk_columns = {c for fk in fks for c in fk["constrained_columns"]}
    unique = {c for constraint in inspector.get_unique_constraints(table) for c in constraint["column_names"]}

    header_h = 0.7
    row_h = 0.34
    height = header_h + max(len(columns), 1) * row_h + 0.25
    box = FancyBboxPatch((x, y - height + 1.0), width, height,
                         boxstyle="round,pad=0.06,rounding_size=0.08",
                         facecolor="#FFFFFF", edgecolor=domain["border"], linewidth=1.1, zorder=4)
    ax.add_patch(box)
    ax.add_patch(FancyBboxPatch((x, y + 1.0 - header_h), width, header_h,
                                boxstyle="round,pad=0.06,rounding_size=0.08",
                                facecolor=domain["color"], edgecolor=domain["color"], zorder=5))
    ax.text(x + width / 2, y + 0.65, table, ha="center", va="center",
            fontsize=9, fontweight="bold", color="white", zorder=6)

    bottom = y + 1.0 - header_h - 0.18
    for index, column in enumerate(columns):
        name = column["name"]
        key = ""
        if name in pk: key += "[PK] "
        if name in fk_columns: key += "[FK] "
        if name in unique: key += "[UQ] "
        text = f"{key}{name}: {column['type']}"
        color = "#B45309" if key.startswith("[PK]") else ("#7C3AED" if "[FK]" in key else "#1E293B")
        ax.text(x + 0.13, bottom - index * row_h, text, ha="left", va="top",
                fontsize=6.5, color=color, zorder=6)
    return height


if __name__ == "__main__":
    main()
    print(OUTPUT_STEM + ".png/.svg/.pdf and " + OUTPUT_STEM + "_INVENTORY.md created")
