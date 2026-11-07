# Hydro Geo

<!--
FICTIONAL SAMPLE. This person, their projects and their numbers are invented.
Use it to try tailor_cv.py, or as a template for your own master_cv.md (which is git-ignored).

How a master CV differs from a normal CV:
- It holds MORE detail than any CV you'd send: every project, method, tool and number.
  The tailor selects and rewrites from it; it can only use what is written here.
- Every claim must be true. The tailor is told never to add skills, numbers, titles or dates.
- Mark the depth of each skill honestly (see "Limited exposure"), so the tailor keeps qualifiers.
-->

Environmental Data Scientist | PhD, Hydrology
Seattle, WA | hydro.geo@example.com
LinkedIn: (your profile URL) | GitHub: (your profile URL)

## Summary (source material, the tailor rewrites this per job)

Hydrology PhD who builds statistical and machine-learning models from noisy environmental sensor data. Built a Python pipeline that cleans and quality-controls data from ~120 river gauges (~40 million readings), and a gradient-boosting model that forecasts 3-day streamflow with lower error than the operational baseline. Experienced in time-series analysis, uncertainty quantification, and communicating results to non-specialist partners.

## Education

- **PhD, Civil and Environmental Engineering (Hydrology)**, Example State University, 2025
  - Thesis: Data-driven forecasting of streamflow in snow-dominated basins
  - Coursework: Statistical Learning; Time Series Analysis; Remote Sensing of the Environment
- **BS, Environmental Science**, Example College, 2019

## Data science & modeling projects

### Streamflow forecasting with gradient boosting
Example State University | 2023–2025

- **Question:** Can machine learning improve 3-day streamflow forecasts over the physics-based model used operationally?
- **Data:** Daily records from 35 basins, 2000–2022: streamflow, precipitation, temperature, snow water equivalent
- **Methods:** Gradient-boosted trees (XGBoost); lagged and rolling-window features; time-based train/test split to avoid leakage; SHAP values to explain predictions
- **Results:** Mean absolute error 18% lower than the operational baseline on held-out years (2019–2022)
- **Tools:** Python (pandas, NumPy, scikit-learn, XGBoost, SHAP, Matplotlib)
- **Role:** Sole developer; results presented to the regional water agency

### Sensor data quality-control pipeline
Example State University | 2022–2024

- **Problem:** River gauge data contained gaps, spikes and drift that were removed by hand
- **What I built:** Python pipeline that flags spikes, flat-lines and drift with rule-based and statistical checks, fills short gaps by interpolation, and writes a QC report per gauge
- **Scale:** ~120 gauges, ~40 million readings
- **Impact:** Replaced a manual monthly review that took about two days; now used by 3 people in the lab
- **Tools:** Python, pandas, SQLite, Git

### Course project: drought index from satellite data
Statistical Learning course | Team of 3

- **My part:** Downloaded and aligned satellite soil-moisture rasters; built a random-forest model of crop stress
- **Teammates' part:** Field data collection and the final report
- **Result:** Model explained about 60% of variance in the test region

## Research & professional experience

### Graduate Research Assistant, Example State University
Seattle, WA | Sep 2019–Aug 2025

- Led the streamflow forecasting and QC pipeline projects above
- Analyzed sensor data with time-series decomposition, change-point detection and bootstrap confidence intervals
- Mentored 2 undergraduate researchers in Python and data cleaning

### Summer Intern, Example Water Agency
Remote | Jun–Aug 2022

- Built dashboards in Python (Plotly) for weekly reservoir reports used by 4 staff

## Technical skills

- **Programming & tools:** Python (pandas, NumPy, scikit-learn, XGBoost, Matplotlib, Plotly), SQL (SQLite), Git, Jupyter
- **Statistics & ML:** Gradient boosting, random forests, linear and logistic regression, time-series decomposition, change-point detection, bootstrap, SHAP
- **Geospatial:** Raster data (rasterio, xarray), QGIS
- **Limited exposure (coursework level, do not overstate):** PyTorch (one course assignment), cloud computing (a single AWS tutorial)
- **No experience:** Spark, A/B testing, production ML deployment
- **Languages:** English, Spanish

## Publications

- Geo, H., & Example, A. (2024). Gradient boosting for short-range streamflow forecasting in snow-dominated basins. *Example Journal of Hydrology*, 12, 100–115.

## Awards

- Graduate Research Fellowship, Example State University (2021)
