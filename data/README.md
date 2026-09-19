# Survey data requirements

Place the encoded SPSS survey file in this directory only for local work. The
directory is configured so that raw data files are not committed by default.

## Required variables

The survey-regression notebook uses the following constructs:

| Construct | Expected survey item |
| --- | --- |
| Age | Q6 or a column whose label contains `请问您的年龄` |
| Monthly income | Q7 or a column whose label contains `月收入是多少` |
| Commute distance | `Q9` |
| Vehicle ownership | Q10 or a column whose label contains `车辆保有量` |
| Minimum acceptable discount | Q16 or matching label |
| Willingness to try ride-pooling | Q24 or matching label |
| Willingness to share with strangers | Q29 or matching label |
| Willingness to pay | Q33 or matching label |
| Maximum willingness to pay | Q34 or matching label |

The operational notebook directly requires `Q16`, `Q29`, `Q33`, and `Q34`.

## Coding used by the notebooks

- `Q16`: `1`, `2`, and `3` map to minimum acceptable discounts `0.25`,
  `0.35`, and `0.45`; `4` means never accept.
- `Q24`: original scale `1` (very willing) to `5` (very unwilling), reversed
  in the regression as `try_willing = 6 - try_pool_code`.
- `Q29`: reversed as `share_willing = 6 - stranger_code`.
- `Q33`: `2` means not willing to pay; a missing `Q34` is then assigned to the
  zero-WTP class.
- `Q34`: `1` = `<5 RMB`, `2` = `5–10 RMB`, `3` = `10–20 RMB`, and
  `4` = `>20 RMB`.

Do not change these mappings without updating the study methods and rerunning
all reported analyses.

## Public-release check

Before adding any respondent-level file, verify all of the following:

- public sharing is covered by participant consent;
- ethics approval and institutional rules permit redistribution;
- direct and indirect identifiers have been removed;
- free-text fields and file metadata have been reviewed;
- the repository license is compatible with the data owner's terms.

Code and data may need different licenses. If public data release is not
permitted, keep the raw file private and publish a data availability statement.
