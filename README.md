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

## ICTTE 2026 conference-paper scenario correspondence

The ICTTE conference paper reports a **two-scenario comparison** selected from the
three configurations available in the operational notebook. The labels are
**not identical** between the paper and the notebook:

| ICTTE paper label | Notebook label | Acceptance specification |
| --- | --- | --- |
| **Scenario A — Fixed-threshold homogeneous** | **Scenario B — Homogeneous behaviour** | `delta_bar = 0.35`, `omega_bar = 0.25` in the reported benchmark |
| **Scenario B — Survey-informed heterogeneous** | **Scenario C — Survey-informed heterogeneous behaviour** | Complete respondent profiles, including minimum-discount and WTP thresholds |

**Notebook Scenario A — Universal acceptance** is an auxiliary baseline and
is **not** one of the paper's two reported scenarios. The notebook uses a
three-scenario naming scheme for broader exploratory analysis; do not read the
paper's Scenario A as notebook Scenario A.

In the conference-paper comparison, the 75% upfront discount is an illustrative
experimental benchmark, not a market-estimated discount. The service-rate
difference between the fixed-threshold and survey-informed cases reflects
**both aggregate acceptance differences and individual threshold dispersion**;
it should not be interpreted as the isolated causal effect of heterogeneity.

The main scale comparison and the discount/WTP sensitivity experiments use
separate profile draws/seeds, so their nominally identical 75% settings can
have different Monte Carlo estimates. The paper must identify each result by
its experiment rather than silently treating those values as identical.

## Implementation details relevant to the paper

- WTP is elicited for a 10 km trip with a RMB 30 solo fare, and transferred
  using the reported WTP-to-RMB-30 ratio.
- The open-ended Q34 category above RMB 20 has **an assumed RMB 30 upper
  bound** in the code (`Q34_OPEN_UPPER_CAP_RMB = 30.0`). This is a modelling
  assumption, not a survey-measured upper limit; WTP sensitivity should be
  interpreted accordingly.
- In `gamma_settlement`, conditions are evaluated sequentially: first
  `total_distance <= BASE_DISTANCE_KM`; otherwise
  `shared_distance <= BASE_DISTANCE_KM`; otherwise the final branch.
  Hence the paper's piecewise conditions must be non-overlapping and match
  that `if/elif/else` precedence.
- Equation (7) in the paper describes the distance–service formulation; the
  implementation uses an online greedy minimum-incremental-distance insertion
  heuristic and **does not** solve a full-horizon MIP.
- The respondent-level survey file is not public. Consequently, this
  repository documents the implementation but does **not** provide independent
  full reproduction of the reported empirical numerical results.

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
