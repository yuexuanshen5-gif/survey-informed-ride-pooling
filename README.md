# Survey-Informed Ride-Pooling Models

This repository contains the reproducible analysis code for a survey-informed
ride-pooling study. It links stated passenger preferences to an operational
ride-pooling simulation.

The repository contains two notebooks:

1. `notebooks/01_survey_regression.ipynb` estimates ordinal logistic models of
   ride-pooling willingness from the survey responses.
2. `notebooks/02_operational_model.ipynb` implements the unified insertion,
   pricing, acceptance, settlement, Monte Carlo, and synthetic scaling
   experiments for Scenarios A/B/C.

## Model overview

The operational notebook applies the same routing and pricing logic in all
three scenarios. Only the passenger behavioural parameterisation changes:

- **Scenario A — Universal acceptance:**
  $\delta_i=0$ and $WTP_i^{trip}=+\infty$.
- **Scenario B — Homogeneous behaviour:**
  $\delta_i=\bar{\delta}$ and
  $WTP_i^{trip}=\bar{\omega}P_i^{solo}$.
- **Scenario C — Survey-informed heterogeneous behaviour:**
  $\delta_i=\delta_i^{survey}$ and
  $WTP_i^{trip}=\omega_i^{survey}P_i^{solo}$.

The upfront pooled-service offer is

$$
P_{ic}^{offer}=(1-\rho)P_i^{solo},
$$

and the realised settlement is

$$
P_i^{final}=\min(P_i^{offer},P_i^\gamma).
$$

## Repository structure

```text
survey-informed-ride-pooling/
├── .github/workflows/validate-notebooks.yml
├── data/README.md
├── notebooks/
│   ├── 01_survey_regression.ipynb
│   └── 02_operational_model.ipynb
├── outputs/.gitkeep
├── scripts/validate_notebooks.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## Data availability

The respondent-level SPSS file is **not included** in this public repository.
Before releasing it, confirm that the participant consent, ethics approval, and
data-owner permissions allow public redistribution. See `data/README.md` for
the required variables and coding.

To reproduce the exact reported results, use the encoded survey file employed
in the study. If that file cannot be shared, publish an appropriate data
availability statement and, if permitted, a de-identified aggregate or
synthetic demonstration dataset separately.

## Run in Google Colab

The notebooks were designed for Google Colab.

1. Open the notebook from GitHub or upload it to Colab.
2. Run the cells from top to bottom.
3. When prompted, upload the encoded `.sav` survey file.
4. Download the generated CSV and PNG files before closing the Colab session.

Recommended order:

1. `01_survey_regression.ipynb`
2. `02_operational_model.ipynb`

## Run locally

Python 3.10 or later is recommended.

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

The existing upload cells use `google.colab.files`. For local execution, replace
the upload cell with a local path assignment, for example:

```python
sav_path = "data/survey_encoded.sav"
```

Do not commit the survey file unless public redistribution has been explicitly
approved.

## Main generated outputs

The survey-regression notebook writes:

- `fig_main_forest_plot.png`
- `ordinal_model_comparison.csv`
- `ordinal_logit_results.csv`

The operational notebook writes the scenario summaries, Monte Carlo results,
discount and WTP sensitivity tables, request-level results, and synthetic
large-scale experiment tables/figures defined in its final cells.

Generated outputs are ignored by default because some tables may contain
respondent indices or derived respondent-level information. Review each file
before deciding whether to publish it.

## Reproducibility notes

- Random-number generators use explicit seeds in the operational notebook.
- The clean public notebooks contain no execution output, embedded raw data, or
  bundled empirical results from the private survey.
- `scripts/validate_notebooks.py` checks notebook structure, Python syntax, and
  confirms that public notebooks have no stored outputs.
- `rho`, `delta_i`, `omega_i`, `WTP_i^{trip}`, `P_i^{solo}`,
  `P_{ic}^{offer}`, `P_i^\gamma`, and `P_i^{final}` retain the notation used in
  the model.

## License and citation

The code is released under the MIT License. If you use this repository in
academic work, please cite the associated paper. Add the final paper citation,
DOI, and a `CITATION.cff` file once those details are available.

## Known limitation

Exact end-to-end reproduction requires the original encoded survey data, which
is not bundled here. The notebooks should therefore be described as open code;
do not claim fully open data or fully push-button reproducibility unless an
approved public dataset is also released.
