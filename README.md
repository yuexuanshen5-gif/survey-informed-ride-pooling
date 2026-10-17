# Survey-Informed Evaluation of Ride-Pooling Operations under Heterogeneous Passenger Acceptance

**Research code accompanying an ICTTE 2026 conference manuscript**

**Authors:** Yuexuan Shen (University of New South Wales) and Linfeng Gao (The University of Sydney). The authors contributed equally to the study.

This repository contains the Python notebooks for a survey-informed ride-pooling study. We examine a simple but important distinction: **a route-feasible pooled trip is not necessarily a trip that a passenger will accept**. By incorporating respondent-specific fare-discount requirements and willingness-to-pay (WTP) thresholds into an online matching simulation, we compare estimated service and operational outcomes under homogeneous versus survey-informed passenger assumptions.

> **Scope:** The survey preferences are drawn from 205 respondents, while the demand, fleet, and trip instances are synthetic. The reported results are controlled simulation outcomes, **not forecasts of real-world ride-pooling adoption**.

## Key findings from the manuscript

At a **75% upfront fare discount** (an experimental benchmark, not an estimated market discount), the survey-informed scenario produced lower realised service rates than the homogeneous scenario at all three synthetic demand–fleet scales:

| Demand–fleet scale | Requests / vehicles | Homogeneous (paper Scenario A) | Survey-informed (paper Scenario B) | Relative reduction |
| --- | ---: | ---: | ---: | ---: |
| Low | 50 / 15 | 57.20% | 33.68% | 41.1% |
| Medium | 100 / 30 | 62.20% | 37.08% | 40.4% |
| High | 200 / 60 | 71.00% | 40.68% | 42.7% |

Additional findings:

- **Acceptance matters alongside routing:** at the High scale, the survey-informed simulation classified 35.68% of requests as passenger-unacceptable and 23.64% as route-infeasible at the benchmark discount.
- **Fare responses differ:** homogeneous thresholds create a sharp participation cutoff, while complete survey-informed profiles yield a more gradual change in realised service as the offered discount increases.
- **WTP treatment matters:** for the High-scale 75% case, the survey-informed mean service rate ranged from 19.84% under lower-bound WTP to 58.88% under midpoint WTP in separate sensitivity runs; random WTP sampling yielded 42.30%.
- **Operational metrics should be interpreted jointly:** lower VKT or revenue under the survey-informed scenario partly reflects fewer accepted trips, not necessarily a more efficient service.

**Interpretation cautions:** The two scenarios differ in both aggregate acceptance propensity and individual threshold dispersion; their service-rate gap is **not** an isolated causal effect of heterogeneity. Separately seeded/profile-resampled experiments also explain why the High-scale survey-informed result at 75% is **40.68% in the main scale comparison**, **39.36% in the discount sensitivity**, and **42.30% in the random-WTP sensitivity**.

## Methodology

### 1. Survey-informed passenger profiles

The study uses **205 stated-/revealed-preference (SP/RP) respondent profiles**. Each complete record preserves the observed combination of minimum acceptable pooling discount, WTP, willingness to share with strangers, and travel/demographic characteristics. Profiles are sampled **as complete rows with replacement** for synthetic requests to retain their within-respondent associations.

In the survey, 22 respondents required at least a 25% discount, 87 required 35%, 75 required 45%, and 21 indicated they would never accept pooling. WTP was elicited for a **10 km trip with an RMB 30 solo fare**, then converted into a transferable trip-specific affordability ratio. WTP is interval-reported: the open-ended category above RMB 20 is given an **assumed RMB 30 upper cap**, not an observed survey limit. Lower-bound, midpoint, upper-bound, and random-within-interval treatments are considered in sensitivity analysis.

The survey notebook separately fits **ordinal logistic regression** models to diagnose associations between respondent characteristics and stated willingness. Its fitted probabilities **are not used as operational acceptance probabilities**.

### 2. Sequential online matching and pricing

The operational notebook models arriving requests and feasible pickup/drop-off insertions. Each feasible offer is evaluated against the assigned passenger's minimum discount and WTP limit. An accepted request updates the vehicle state; rejected offers do not become realised services.

The simulation uses an **online greedy minimum-incremental-distance insertion heuristic** under waiting-time, detour, and vehicle-capacity constraints. Although the manuscript presents a distance–service mathematical formulation, **the code does not solve a full-horizon mixed-integer program**.

Upfront acceptance and ex-post fare settlement are deliberately separated. The implementation uses the following notation:

$$
P_{ic}^{offer}=(1-\rho)P_i^{solo},
$$

$$
P_i^{final}=\min(P_i^{offer},P_i^\gamma).
$$

In `gamma_settlement`, the implementation checks `total_distance <= BASE_DISTANCE_KM` first, then `shared_distance <= BASE_DISTANCE_KM`, then the remaining case. This precedence is important when interpreting the piecewise settlement formula.

### 3. Controlled simulation design

The paper compares three synthetic scales (50/15, 100/30, and 200/60 requests/vehicles). Each scale uses **five demand–fleet seeds**. The homogeneous scenario runs once per seed; the survey-informed scenario uses **five respondent-profile assignments per seed** (25 realisations per scale). Within a shared seed, the generated demand, fleet, route-feasibility rules, and pricing are held fixed.

Reported outcomes include realised service rate, route-infeasible versus passenger-unacceptable rejections, vehicle kilometres travelled (VKT), distance-weighted occupancy, and revenue. Discount and WTP sensitivity experiments use separate experimental draws.

## Important: paper versus notebook scenario labels

The operational notebook has **three configurations**, but the ICTTE manuscript reports **two**. The letter labels do **not** correspond directly:

| ICTTE manuscript | Operational notebook | Meaning |
| --- | --- | --- |
| **Scenario A** | **Scenario B** | Homogeneous: fixed discount and WTP thresholds (reported benchmark: `delta_bar = 0.35`, `omega_bar = 0.25`) |
| **Scenario B** | **Scenario C** | Survey-informed: respondent-specific minimum discounts and WTP limits, assigned as complete profiles |
| *Not included in the paper comparison* | **Scenario A** | Auxiliary universal-acceptance baseline |

For the notebook's general notation:

- **Notebook Scenario A:** `\delta_i=0` and `WTP_i^{trip}=+\infty`.
- **Notebook Scenario B:** `\delta_i=\bar{\delta}` and `WTP_i^{trip}=\bar{\omega}P_i^{solo}`.
- **Notebook Scenario C:** `\delta_i=\delta_i^{survey}` and `WTP_i^{trip}=\omega_i^{survey}P_i^{solo}`.

When comparing results with the manuscript, use the **paper-to-notebook mapping above** rather than matching scenario letters directly.

## Repository contents

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
├── PUBLISHING_GUIDE_zh-CN.md
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

- [`01_survey_regression.ipynb`](notebooks/01_survey_regression.ipynb): survey coding, ordinal logistic models, model comparisons, odds ratios, and a forest plot.
- [`02_operational_model.ipynb`](notebooks/02_operational_model.ipynb): insertion and route-feasibility logic, upfront acceptance, ex-post pricing, Scenarios A/B/C, Monte Carlo runs, and synthetic scaling and sensitivity experiments.
- [`data/README.md`](data/README.md): required SPSS survey variables and coding rules.
- [`scripts/validate_notebooks.py`](scripts/validate_notebooks.py): structural/syntax and stored-output checks for the public notebooks.

## How to run

### Option 1 — Google Colab

The notebooks are written primarily for Google Colab.

1. Open [the survey notebook](notebooks/01_survey_regression.ipynb) in Colab and run its cells in order.
2. When requested, supply an **authorised, encoded** `.sav` survey file; the original respondent data are not distributed here.
3. Open [the operational notebook](notebooks/02_operational_model.ipynb) and repeat the authorised survey upload when prompted.
4. Run the notebook cells in order, including the large-scale and sensitivity sections as needed.
5. Save generated figures and CSV files before the Colab session ends.

The original encoded survey data are necessary to reproduce the manuscript's numerical outcomes.

### Option 2 — Local Python environment

Python **3.10+** is recommended.

```bash
git clone https://github.com/yuexuanshen5-gif/survey-informed-ride-pooling.git
cd survey-informed-ride-pooling
python -m venv .venv
```

Activate the environment (macOS/Linux: `source .venv/bin/activate`; Windows PowerShell: `.venv\Scripts\Activate.ps1`), then run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

For local execution, adapt the notebooks' `google.colab.files` upload cells to read an authorised file from a local path, such as `data/survey_encoded.sav`. Do not commit this file.

## Outputs and reproducibility

The survey notebook generates outputs including `fig_main_forest_plot.png`, `ordinal_model_comparison.csv`, and `ordinal_logit_results.csv`. The operational notebook exports simulation summaries, request-level outcomes, Monte Carlo tables, discount/WTP sensitivity results, and figures from its final sections.

- Seeds are explicitly set in the operational notebook, but sampling-based experiments still depend on the authorised input data and experiment configuration.
- Public notebook files are stored **without execution outputs or embedded respondent-level data**.
- Generated outputs are ignored by default and should be checked for potentially sensitive respondent identifiers or derived individual records before public release.
- The private respondent-level SPSS survey file is **not publicly available due to participant privacy restrictions**. Code availability does **not** imply fully independent reproduction of the empirical results.

## Limitations

This is a controlled, **survey-informed synthetic simulation**, not a field validation. The respondent sample may not represent the wider travelling population; reported WTP values are intervals; passenger acceptance is modelled using deterministic thresholds; and online greedy insertion is not system-wide optimisation. Generalisations to observed demand, actual bookings, or other fleets and networks require further validation.

## Citation and license

**Associated manuscript (ICTTE 2026):**

Shen, Y., and Gao, L. *Survey-Informed Evaluation of Ride-Pooling Operations under Heterogeneous Passenger Acceptance*. ICTTE 2026 manuscript.

Please use the final proceedings citation and DOI once available; no DOI or formal publication status is asserted here.

Code is available under the repository's [MIT License](LICENSE). The survey data are **not** covered by permission to redistribute the code and must not be added without the relevant consent, ethics, and data-owner approvals.
