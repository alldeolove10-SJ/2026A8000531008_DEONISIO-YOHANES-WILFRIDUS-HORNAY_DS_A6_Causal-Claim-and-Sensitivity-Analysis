# 2026A8000531008_DEONISIO-YOHANES-WILFRIDUS-HORNAY_DS_A6_Causal-Claim-and-Sensitivity-Analysis

# DS-A6: Causal Claim and Sensitivity Analysis

## 1. Project Overview

This project explores causal analysis using a synthetic tutoring example. It looks at the relationship between tutoring and student exam scores and examines how different assumptions can affect the results.

The main purpose is to understand the difference between finding a relationship in data and making a causal claim.

## 2. Project Structure

The repository contains the following folders and files:

- `data/` - Contains the synthetic dataset and its provenance information.
- `figures/` - Contains graphs generated during the analysis.
- `notebooks/` - Contains the Jupyter Notebook used for the project.
- `report/` - Contains the project report in Word and PDF formats.
- `results/` - Contains CSV files with estimates, assumptions, and sensitivity analysis results.
- `src/` - Contains the Python script used for the analysis.
- `DATA_DICTIONARY.md` - Explains the variables in the dataset.
- `README.md` - Provides an overview of the project.

## 3. Dataset

The dataset is stored in `data/synthetic_tutoring_example.csv`.

It contains synthetic data created for this project. The data represents an example of students, tutoring participation, and exam performance. It is not collected from real students.

The file `data/DATA_PROVENANCE.md` provides further information about how the dataset was created.

## 4. Method

The analysis follows these main steps:

1. Load and check the dataset.
2. Explore the relationship between tutoring and exam scores.
3. Estimate the effect of tutoring using regression models.
4. Compare results before and after adjusting for selected variables.
5. Examine possible omitted-variable bias.
6. Use sensitivity analysis to see how different assumptions affect the estimates.
7. Create graphs and tables to summarize the results.

## 5. Figures

The `figures/` folder contains the following graphs:

- `01_demo_estimate_comparison.png` - Compares the estimated effects.
- `02_demo_sensitivity_curve.png` - Shows how estimates change under different sensitivity assumptions.
- `03_demo_outcome_distributions.png` - Displays the outcome distributions.
- `04_demo_dag.png` - Shows the causal diagram used in the analysis.

## 6. Results

The `results/` folder contains three main files:

- `demo_assumptions_table.csv` - Summarizes the assumptions used in the analysis.
- `demo_estimates.csv` - Contains the estimated effects.
- `demo_omitted_bias_sensitivity.csv` - Contains the results of the omitted-variable bias sensitivity analysis.

These files provide more detail about the calculations and comparisons made in the notebook.

## 7. How to Run

### Requirements

- Python 3.11 or later
- pandas
- NumPy
- Matplotlib
- statsmodels
- Jupyter Notebook

Install the required libraries with:

```bash
pip install pandas numpy matplotlib statsmodels jupyter
```

### Run the Notebook

Open a terminal in the main project folder and run:

```bash
jupyter notebook notebooks/DS_A6_Causal_Claim_Sensitivity.ipynb
```

Run the notebook cells in order to perform the analysis and view the results.

The Python script is located at `src/demo_causal_sensitivity.py`.

## 8. Report

The `report/` folder contains the project report in Word and PDF formats. It explains the analysis, the assumptions used, and the limitations of the causal conclusions.

## 9. Conclusion

This project shows that estimating a causal effect requires more than comparing two groups. The results can depend on the variables included in the model and the assumptions made about possible confounding factors.

Sensitivity analysis helps show how reliable a causal conclusion may be when some assumptions cannot be fully verified.
