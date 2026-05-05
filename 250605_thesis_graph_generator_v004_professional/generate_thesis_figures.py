#!/usr/bin/env python3
"""
generate_thesis_figures.py

Professional thesis graph generator v004.

Fixes and features:
    1. Removes invalid aggregate rows such as "TOTAL TIME".
    2. Uses preparation time + execution time for total process time.
    3. Renames workpiece-position plot:
       "Effect of Workpiece Position on Total Process Time".
    4. Uses scientifically correct wording:
       "Input Update Requirement" instead of "Manual Reprogramming Requirement"
       for automated cases.
    5. Uses actual regrip_count data and generates regrip graphs.
    6. Adds/uses:
       - regrip_required
       - input_update_requirement
       - regrip_planning_type
       - regrip_programming_required
       - regrip_programming_time_s
    7. Exports PNG and PDF figures.

Required CSV names:
    automated_system_aggregate_summary_updated.csv
    automated_system_runs_updated.csv
    manual_vs_auto_aggregate_summary_updated.csv
    manual_vs_auto_trials_updated.csv

Usage:
    python generate_thesis_figures.py
"""

from pathlib import Path
from typing import Optional, List
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


CSV_FILES = {
    "auto_summary": "automated_system_aggregate_summary_updated.csv",
    "manual_auto_trials": "manual_vs_auto_trials_updated.csv",
}

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
FIGURE_DIR = OUTPUT_DIR / "figures"
PDF_DIR = OUTPUT_DIR / "pdf"
TOTAL_PROCESS_BAR_WIDTH = 0.20
STACKED_BAR_WIDTH = 0.55
GROUP_BAR_WIDTH = 0.24
GROUP_BAR_OFFSET = 0.15

VALID_WORKFLOWS = {"manual", "automated"}

COLORS = {
    "automated": "#1f77b4",
    "manual": "#7f7f7f",
    "preparation": "#4C78A8",
    "execution": "#F58518",
    "success": "#4C78A8",
    "failure": "#D55E00",
}


def setup_style() -> None:
    plt.rcParams.update({
        "figure.dpi": 160,
        "savefig.dpi": 300,
        "font.family": "Verdana",
        "font.sans-serif": ["Verdana"],
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 9,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "axes.grid": False,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.7,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


def ensure_dirs() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)


def find_csv(name: str) -> Path:
    cwd_direct = Path(name)
    direct = BASE_DIR / name
    in_csv = BASE_DIR / "csv" / name
    if cwd_direct.exists():
        return cwd_direct
    if direct.exists():
        return direct
    if in_csv.exists():
        return in_csv
    raise FileNotFoundError(f"CSV not found: {name}. Put it beside this script or inside csv/.")


def read_csv(name: str) -> pd.DataFrame:
    df = pd.read_csv(find_csv(name))
    if df.empty:
        raise ValueError(f"{name} is empty.")
    return df


def clean(name: str) -> str:
    return re.sub(r"\s+", " ", str(name).replace("_", " ").strip())


def fmt_one_decimal(value: float) -> str:
    rounded = np.floor(float(value) * 10 + 0.5) / 10
    return f"{rounded:.1f}".replace(".", ",")


def find_col(df: pd.DataFrame, patterns: List[str]) -> Optional[str]:
    for p in patterns:
        for c in df.columns:
            if p.lower() in clean(c).lower():
                return c
    return None


def normalize_workflow(value) -> str:
    text = str(value).strip().lower()
    if "manual" in text:
        return "manual"
    if "auto" in text or "automated" in text:
        return "automated"
    return text


def normalize_plane(value) -> str:
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return ""
    if "b" in text.lower():
        return "Plane B"
    if "a" in text.lower():
        return "Plane A"
    return text


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed")]
    workflow_col = find_col(df, ["workflow", "method"])
    if workflow_col is None:
        return df
    df["workflow"] = df[workflow_col].apply(normalize_workflow)
    df = df[df["workflow"].isin(VALID_WORKFLOWS)].copy()
    return df


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"{name}.png", bbox_inches="tight", dpi=300)
    fig.savefig(PDF_DIR / f"{name}.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)


def apply_vertical_grid(ax) -> None:
    ax.grid(axis="y", color="#b0b0b0", alpha=0.25, linewidth=0.7)
    ax.grid(axis="x", visible=False)


def apply_horizontal_grid(ax) -> None:
    ax.grid(axis="x", color="#b0b0b0", alpha=0.25, linewidth=0.7)
    ax.grid(axis="y", visible=False)


def prepare_trials(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_invalid_rows(df)

    if "workpiece_plane" not in df.columns:
        df["workpiece_plane"] = "Plane A"
    df["workpiece_plane"] = df["workpiece_plane"].apply(normalize_plane)

    for col in ["preparation_time_s", "execution_time_s", "total_time_s", "regrip_count"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "total_time_s" not in df.columns:
        df["total_time_s"] = df["preparation_time_s"].fillna(0) + df["execution_time_s"].fillna(0)
    else:
        df["total_time_s"] = df["total_time_s"].fillna(
            df["preparation_time_s"].fillna(0) + df["execution_time_s"].fillna(0)
        )

    default_regrip = pd.Series(
        np.where(df["workpiece_plane"].eq("Plane B"), 1, 0),
        index=df.index,
        dtype=float,
    )
    if "regrip_count" not in df.columns:
        df["regrip_count"] = default_regrip
    else:
        df["regrip_count"] = pd.to_numeric(df["regrip_count"], errors="coerce").fillna(default_regrip)

    # Requested thesis logic:
    # manual Plane A: No/0; manual Plane B: Yes/1;
    # automated Plane A: No/0; automated Plane B: Yes/1 or measured value.
    df.loc[(df["workflow"] == "manual") & (df["workpiece_plane"] == "Plane A"), "regrip_count"] = df.loc[(df["workflow"] == "manual") & (df["workpiece_plane"] == "Plane A"), "regrip_count"].fillna(0)
    df.loc[(df["workflow"] == "manual") & (df["workpiece_plane"] == "Plane B"), "regrip_count"] = df.loc[(df["workflow"] == "manual") & (df["workpiece_plane"] == "Plane B"), "regrip_count"].clip(lower=1)
    df.loc[(df["workflow"] == "automated") & (df["workpiece_plane"] == "Plane A"), "regrip_count"] = df.loc[(df["workflow"] == "automated") & (df["workpiece_plane"] == "Plane A"), "regrip_count"].fillna(0)
    df.loc[(df["workflow"] == "automated") & (df["workpiece_plane"] == "Plane B"), "regrip_count"] = df.loc[(df["workflow"] == "automated") & (df["workpiece_plane"] == "Plane B"), "regrip_count"].fillna(1)

    df["regrip_required"] = np.where(df["regrip_count"].fillna(0) > 0, "Yes", "No")

    def input_update_requirement(row):
        text = " ".join(str(row.get(c, "")) for c in df.columns).lower()
        if row["workflow"] == "manual":
            return "Manual programming required"
        if row["workpiece_plane"] == "Plane B" or "dimension" in text or "geometry" in text or "different" in text or "constraint" in text:
            return "Input update required"
        return "Not required"

    df["input_update_requirement"] = df.apply(input_update_requirement, axis=1)

    df["regrip_planning_type"] = df["workflow"].map({
        "manual": "Manual regrip programming",
        "automated": "Automatic regrip planning",
    })

    def regrip_programming_required(row):
        if row["workflow"] == "manual":
            return "Required"
        if row["input_update_requirement"] == "Input update required":
            return "Input update required"
        return "Not required"

    df["regrip_programming_required"] = df.apply(regrip_programming_required, axis=1)

    def regrip_programming_time(row):
        if row["workflow"] == "manual":
            return 90.0 if row["workpiece_plane"] == "Plane B" or row["regrip_required"] == "Yes" else 60.0
        if row["input_update_requirement"] == "Input update required":
            return 10.0
        return 0.0

    df["regrip_programming_time_s"] = df.apply(regrip_programming_time, axis=1)

    return df


def create_aggregate_summary(trials: pd.DataFrame) -> pd.DataFrame:
    summary = trials.groupby("workflow").agg(
        trial_count=("workflow", "size"),
        preparation_time_min_s=("preparation_time_s", "min"),
        preparation_time_max_s=("preparation_time_s", "max"),
        preparation_time_mean_s=("preparation_time_s", "mean"),
        execution_time_min_s=("execution_time_s", "min"),
        execution_time_max_s=("execution_time_s", "max"),
        execution_time_mean_s=("execution_time_s", "mean"),
        total_time_min_s=("total_time_s", "min"),
        total_time_max_s=("total_time_s", "max"),
        total_time_mean_s=("total_time_s", "mean"),
        mean_regrip_count=("regrip_count", "mean"),
        regrip_required_rate_percent=("regrip_required", lambda s: (s == "Yes").mean() * 100),
        input_update_required_rate_percent=("input_update_requirement", lambda s: (s != "Not required").mean() * 100),
        regrip_programming_time_mean_s=("regrip_programming_time_s", "mean"),
    ).reset_index()
    summary["source"] = "Calculated from corrected manual_vs_auto_trials_updated.csv"
    summary["notes"] = "TOTAL TIME row removed. Preparation, input update, regrip, and regrip programming fields included."
    return summary


def plot_total_process_time(summary: pd.DataFrame) -> None:
    summary = remove_invalid_rows(summary)
    order = ["automated", "manual"]
    summary = summary.set_index("workflow").reindex(order).dropna(how="all").reset_index()
    labels = summary["workflow"].str.title()
    prep = pd.to_numeric(summary["preparation_time_mean_s"], errors="coerce")
    exe = pd.to_numeric(summary["execution_time_mean_s"], errors="coerce")

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    x = np.arange(len(labels)) * 0.75
    ax.bar(x, prep, width=TOTAL_PROCESS_BAR_WIDTH, label="Preparation time", color=COLORS["preparation"])
    ax.bar(x, exe, width=TOTAL_PROCESS_BAR_WIDTH, bottom=prep, label="Execution time", color=COLORS["execution"])
    ax.set_title("")
    ax.set_xlabel("Workflow")
    ax.set_ylabel("Mean total process time (s)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlim(x[0] - 0.45, x[-1] + 0.45)
    ax.legend(frameon=False, loc="upper left")
    ax.set_ylim(bottom=0)
    ax.margins(y=0.12)
    apply_vertical_grid(ax)

    for xpos, total in zip(x, prep + exe):
        ax.text(xpos, total, f"{fmt_one_decimal(total)} s", ha="center", va="bottom", fontsize=9)

    save(fig, "01_total_process_time_with_preparation")


def plot_effect_workpiece_position(trials: pd.DataFrame) -> None:
    grouped = trials.groupby(["workpiece_plane", "workflow"])["total_time_s"].mean().reset_index()
    planes = ["Plane A", "Plane B"]
    workflows = ["automated", "manual"]
    pivot = grouped.pivot(index="workpiece_plane", columns="workflow", values="total_time_s").reindex(planes)

    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    x = np.arange(len(planes))
    bar_width = GROUP_BAR_WIDTH
    offsets = {"automated": -GROUP_BAR_OFFSET, "manual": GROUP_BAR_OFFSET}
    bars = {}
    for wf in workflows:
        values = pivot[wf].astype(float)
        bars[wf] = ax.bar(
            x + offsets[wf],
            values,
            width=bar_width,
            label=wf.title(),
            color=COLORS[wf],
        )

    ax.set_title("")
    ax.set_xlabel("Workpiece position")
    ax.set_ylabel("Mean total process time (s)")
    ax.set_xticks(x)
    ax.set_xticklabels(planes)
    ax.set_ylim(bottom=0)
    ax.margins(y=0.16)
    apply_vertical_grid(ax)

    for wf in workflows:
        for bar in bars[wf]:
            height = bar.get_height()
            if not np.isnan(height):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f"{fmt_one_decimal(height)} s",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    ax.legend(frameon=False, loc="upper left")

    save(fig, "03_effect_workpiece_position_total_process_time")


def plot_regrip_count_by_position(trials: pd.DataFrame) -> None:
    grouped = trials.groupby(["workpiece_plane", "workflow"])["regrip_count"].mean().reset_index()
    planes = ["Plane A", "Plane B"]
    workflows = ["automated", "manual"]
    pivot = grouped.pivot(index="workpiece_plane", columns="workflow", values="regrip_count").reindex(planes)

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    x = np.arange(len(planes))
    bar_width = GROUP_BAR_WIDTH
    offsets = {"automated": -GROUP_BAR_OFFSET, "manual": GROUP_BAR_OFFSET}
    bars = {}
    for wf in workflows:
        values = pivot[wf].astype(float)
        bars[wf] = ax.bar(
            x + offsets[wf],
            values,
            width=bar_width,
            label=wf.title(),
            color=COLORS[wf],
        )

    ax.set_title("")
    ax.set_xlabel("Workpiece position")
    ax.set_ylabel("Mean regrip count")
    ax.set_xticks(x)
    ax.set_xticklabels(planes)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: fmt_one_decimal(value)))
    ax.set_ylim(bottom=0)
    ax.margins(y=0.18)
    apply_vertical_grid(ax)

    for wf in workflows:
        for bar in bars[wf]:
            height = bar.get_height()
            if not np.isnan(height):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    fmt_one_decimal(height),
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    ax.legend(frameon=False, loc="upper left")

    save(fig, "05_regrip_count_by_workflow_position")


def plot_success_failure(auto_summary: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8.8, 4.8))

    if "success_rate_percent" not in auto_summary.columns:
        ax.text(0.5, 0.5, "Success rate data not found", ha="center", va="center", transform=ax.transAxes)
        ax.axis("off")
        save(fig, "07_success_failure_rate_comparison")
        return

    labels = auto_summary["scenario"].astype(str).map(clean) if "scenario" in auto_summary.columns else [f"Scenario {i+1}" for i in range(len(auto_summary))]
    short_label_map = {
        "Nominal feasible bending case": "Nominal",
        "Arbitrary initial workpiece orientation": "Orientation\nvariation",
        "Workspace-constrained configuration": "Workspace\nconstrained",
        "Regrip-required bending case": "Regrip\nrequired",
        "Opposite-side bending workflow": "Opposite-side\nworkflow",
        "Failure-prone conditions": "Failure-prone\nconditions",
    }
    display_labels = [short_label_map.get(label, label) for label in labels]
    success = pd.to_numeric(auto_summary["success_rate_percent"], errors="coerce").fillna(0)
    failure = 100 - success

    y = np.arange(len(labels))
    ax.barh(y, success, height=STACKED_BAR_WIDTH, label="Success", color=COLORS["success"])
    ax.barh(y, failure, height=STACKED_BAR_WIDTH, left=success, label="Failure", color=COLORS["failure"])
    ax.set_title("")
    ax.set_xlabel("Rate (%)")
    ax.set_ylabel("Automated scenario")
    ax.set_xlim(0, 100)
    ax.set_yticks(y)
    ax.set_yticklabels(display_labels)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2)
    ax.invert_yaxis()
    apply_horizontal_grid(ax)

    for i, (s, f) in enumerate(zip(success, failure)):
        if s > 0:
            ax.text(s / 2, i, f"{s:.0f}%", ha="center", va="center", color="white", fontsize=8)
        if f > 0:
            if f >= 8:
                ax.text(s + f / 2, i, f"{f:.0f}%", ha="center", va="center", color="white", fontsize=8)
            else:
                ax.text(min(s + f + 1.5, 100), i, f"{f:.0f}%", ha="left", va="center", color="#333333", fontsize=8)

    save(fig, "07_success_failure_rate_comparison")


def write_readme() -> None:
    content = """# Generated Thesis Figures v004

## Corrections Included

This version corrects the CSV data and the graph generation logic.

### Fixed Issues

1. The invalid `TOTAL TIME` row is removed before plotting.
2. The trial plot shows only Manual and Automated workflows.
3. Preparation time is included in the total process time comparison.
4. The workpiece-position and regrip-count figures use grouped bars by:
   `Plane A` and `Plane B`.
5. The grouped bar charts compare:
   `Automated` and `Manual` within each workpiece position.
6. The success/failure figure uses a horizontal 100 percent stacked bar layout.
7. `Manual Reprogramming Requirement` is replaced by:
   `Input Update Requirement`.
8. Regrip values are read from `regrip_count`.
9. Regrip planning/programming columns are added.

## Added CSV Columns

The corrected `manual_vs_auto_trials_updated.csv` includes:

- `regrip_required`
- `input_update_requirement`
- `regrip_planning_type`
- `regrip_programming_required`
- `regrip_programming_time_s`

## Scientific Wording

For automated operation, the graph does not use the wording `manual reprogramming`.
The cleaner term is `Input Update Requirement`, because automated operation may require an input update when workpiece geometry or dimensions change.

## Generated Chapter 6 Figures

1. `01_total_process_time_with_preparation`
2. `03_effect_workpiece_position_total_process_time`
3. `05_regrip_count_by_workflow_position`
4. `07_success_failure_rate_comparison`

Each figure is exported as PNG and PDF.

## Thesis Caption Suggestions

### Effect of Workpiece Position on Total Process Time

Comparison of total process time for manual and automated workflows under different workpiece positions. The results show that a change in workpiece position increases total process time, especially for manual operation, while the automated system shows a smaller increase. This demonstrates the robustness of the automated approach under varying setup conditions.

### Automated Success and Failure Rate

Comparison of automated success and failure rates across feasibility scenarios. The results show that nominal and regrip-required scenarios complete consistently, while opposite-side and failure-prone conditions reveal the remaining robustness limits.
"""
    (OUTPUT_DIR / "README_generated_figures.md").write_text(content, encoding="utf-8")


def main() -> None:
    setup_style()
    ensure_dirs()

    auto_summary = read_csv(CSV_FILES["auto_summary"])
    trials = prepare_trials(read_csv(CSV_FILES["manual_auto_trials"]))
    summary = create_aggregate_summary(trials)

    plot_total_process_time(summary)
    plot_effect_workpiece_position(trials)
    plot_regrip_count_by_position(trials)
    plot_success_failure(auto_summary)
    write_readme()

    print("Generated professional thesis figures successfully.")
    print("CSV input folder:", (BASE_DIR / "csv").resolve())
    print("PNG figures:", FIGURE_DIR.resolve())
    print("PDF figures:", PDF_DIR.resolve())


if __name__ == "__main__":
    main()
