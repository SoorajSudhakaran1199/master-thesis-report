# Generated Thesis Figures v004

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
