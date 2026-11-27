---
applyTo: "**/{methodology,methods,analysis,experiments,src,scripts,notebooks}/**"
---

# Methodology and research code

- Tie each design choice to the research question, the relevant literature, and a defensible methodological rationale.
- State assumptions, inclusion/exclusion criteria, data provenance, preprocessing, measures, baselines, and evaluation procedures.
- Preserve raw data. Make transformations explicit, deterministic where practical, and reproducible from documented inputs.
- Use clear names, small functions, and comments for non-obvious analytical decisions; avoid unexplained constants and hidden notebook state.
- Set and report random seeds where relevant. Record software versions and material configuration in the repository's existing environment files.
- Check for leakage, class imbalance, missingness, confounding, and metric limitations where applicable. Do not overstate causal conclusions from observational evidence.
- Separate exploratory analyses from confirmatory or final analyses. Label deviations from the planned methodology and explain their rationale.
- Never fabricate experiment runs, outputs, or metrics. Report failures and limitations transparently.
- Protect personal, licensed, or sensitive data; do not commit it unless repository policy and permissions allow.
