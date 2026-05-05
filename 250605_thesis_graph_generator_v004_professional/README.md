# Thesis Graph Generator Package v004 Professional

## Purpose

This package contains corrected CSV files and a fully updated Python script for generating professional thesis-ready figures.

---

## Main Corrections

- Removed the invalid `TOTAL TIME` row from plotting logic.
- Corrected the trial graph so it only shows Manual and Automated workflows.
- Included preparation time in total process time.
- Renamed the workpiece-position graph to:  
  `Effect of Workpiece Position on Total Process Time`.
- Replaced `Manual Reprogramming Requirement` with:  
  `Input Update Requirement`.
- Added regrip and regrip planning/programming columns.
- Fixed regrip plotting using actual `regrip_count` values.
- Generated PNG and PDF versions of every figure.

---

## Added Columns in Corrected CSV

The corrected `manual_vs_auto_trials_updated.csv` includes:

- `regrip_required`
- `input_update_requirement`
- `regrip_planning_type`
- `regrip_programming_required`
- `regrip_programming_time_s`

---

## Figure → CSV Data Mapping (IMPORTANT)

### 1. 01_total_process_time_with_preparation

**CSV Used:**  
`manual_vs_auto_aggregate_summary_updated.csv`

**Columns Used:**
- `workflow`
- `preparation_time_mean_s`
- `execution_time_mean_s`

**Logic:**  
Mean values per workflow are used.  
Total process time = preparation + execution.

---

### 2. 02_total_time_across_trials

**CSV Used:**  
`manual_vs_auto_trials_updated.csv`

**Columns Used:**
- `workflow`
- `total_time_s`

**Logic:**  
Per-trial total time plotted for manual vs automated workflows.

---

### 3. 03_effect_workpiece_position_total_process_time

**CSV Used:**  
`manual_vs_auto_trials_updated.csv`

**Columns Used:**
- `workflow`
- `workpiece_plane`
- `total_time_s`

**Logic:**  
Mean total time grouped by workflow and workpiece position (Plane A / Plane B).

---

### 4. 04_input_update_requirement

**CSV Used:**  
`manual_vs_auto_trials_updated.csv`

**Columns Used:**
- `workflow`
- `workpiece_plane`
- `input_update_requirement`

**Logic:**  
Converted to percentage:
- Not required → 0%
- Required / Input update → 100%

Grouped by workflow and workpiece position.

---

### 5. 05_regrip_count_by_workflow_position

**CSV Used:**  
`manual_vs_auto_trials_updated.csv`

**Columns Used:**
- `workflow`
- `workpiece_plane`
- `regrip_count`

**Logic:**  
Mean regrip count per workflow and workpiece position.

---

### 6. 06_regrip_programming_time_comparison

**CSV Used:**  
`manual_vs_auto_trials_updated.csv`

**Columns Used:**
- `workflow`
- `workpiece_plane`
- `regrip_programming_time_s`

**Logic:**  
Mean programming/input update time per workflow and case.

---

### 7. 07_success_failure_rate_comparison

**CSV Used:**  
`automated_system_aggregate_summary_updated.csv`

**Columns Used:**
- `scenario`
- `success_rate_percent`

**Logic:**  
Success vs failure (100 − success rate) comparison.

---

### 8. 08_combined_professional_overview

**Source:**  
All generated figures combined into one multi-panel visualization.

---

## Run

```bash
python generate_thesis_figures.py
```

---

## Output

- `output/updated_csv/`
- `output/figures/`
- `output/pdf/`
- `output/README_generated_figures.md`

---

## Thesis Logic

The main process comparison uses:

**Total Process Time = Preparation Time + Execution Time**

This is the correct comparison for workflow efficiency.

Manual operation requires full programming effort.

Automated operation is not described as manual reprogramming.  
The professional term used is:

**Input Update Requirement**

This is more accurate because automated operation may require an input file update when workpiece geometry, dimensions, or position changes.

---

## Key Interpretation for Thesis

- Manual workflow shows higher total time due to preparation and programming effort.
- Automated workflow reduces total time and is more stable across trials.
- Workpiece position change significantly affects manual operation but has limited impact on automated operation.
- Regrip and programming effort are higher in manual workflows.
- Automated systems rely on planning and minimal input updates rather than full reprogramming.