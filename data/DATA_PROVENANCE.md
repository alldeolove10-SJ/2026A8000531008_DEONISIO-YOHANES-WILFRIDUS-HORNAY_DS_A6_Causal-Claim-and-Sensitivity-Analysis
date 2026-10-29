# Synthetic data provenance
- File: `synthetic_tutoring_example.csv`
- Rows: 2400; SHA-256: `5121872846dfeeb667659dbbab9d20f5a9416dbc5adaa0adb46196cc7b961729`
- Generated deterministically with NumPy seed 6042 by `src/demo_causal_sensitivity.py`.
- Synthetic observational example of tutoring and exam score; not a real study and not a public external dataset.
- Generator includes a true effect of +3 score points, measured pre-treatment covariates, an unobserved motivation confounder, a post-treatment mediator, and a pre-treatment negative-control outcome.
- The known data-generating process is for teaching only; the estimates are not evidence about any real education programme.
