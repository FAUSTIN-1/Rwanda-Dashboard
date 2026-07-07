# 🇷🇼 Rwanda DHS 2019–20 Dashboard

**National Health and Demographic Intelligence**

An interactive, production-grade Streamlit dashboard built entirely from the Rwanda Demographic and Health Survey (DHS) 2019–20 microdata. Designed to the visual and analytical standard expected by international health and development organizations (WHO, UNICEF, NISR, USAID, UNDP, World Bank).

**Author:** Faustin NIZEYIMANA — Statistician and Data Analyst

---

## 1. Project Overview

The Rwanda DHS 2019–20 Dashboard transforms raw DHS survey microdata (Women, Household, and Children recodes) into an executive-ready analytics platform. It provides real-time, province-level exploration of fertility, family planning, maternal and child health, HIV testing, household infrastructure, and socioeconomic indicators — all computed live from the underlying microdata rather than hard-coded figures.

## 2. Objectives

- Provide a single, authoritative, interactive view of Rwanda's 2019–20 demographic and health indicators.
- Enable province-level disaggregation across all five provinces of Rwanda (Kigali City, Southern, Eastern, Northern, Western).
- Replace static reporting with dynamic, filterable, exportable analytics.
- Meet the visual and engineering standards expected of international health-data platforms.

## 3. Key Features

- **Executive header** with national branding and author attribution.
- **Five KPI cards**: Family Planning, Child Nutrition, HIV Tested, Health Insurance, Fertility — all recalculated live from microdata.
- **Province filter system** (replacing tab navigation): National, Kigali City, Southern, Eastern, Northern, Western.
- **Interactive choropleth map** of Rwanda with a 6-indicator dropdown (Modern Contraceptive Prevalence, Child Stunting, Health Insurance Coverage, HIV Testing, Fertility Rate, Skilled Antenatal Care), hover tooltips with sample sizes, and a professional sequential color scale.
- **16+ publication-quality visualizations**: population pyramid, age histogram, fertility trend, maternal care cascade (funnel), family planning awareness funnel, child nutrition breakdown, wealth donut, education donut, wealth × residence treemap, education × wealth heatmap, household infrastructure ranking, province comparison grouped bars, lollipop ranking chart, radar profile, urban/rural slope chart, and ranked horizontal bar chart.
- **Searchable, sortable, paginated data tables** for Women, Households, and Children datasets, each with CSV export.
- **Fully custom UI**: white background, deep-blue header, rounded KPI cards, subtle shadows, hover animations, Inter typography — no default Streamlit chrome.
- **Modular, cache-optimized architecture** with clean separation of data, calculations, and presentation layers.

## 4. Dataset Description

Source: `data/rwanda_dhs_2019_20.xlsx` — a cleaned Rwanda DHS 2019–20 workbook containing:

| Sheet | Description | Records |
|---|---|---|
| Women (IR) | Women aged 15–49: fertility, family planning, health, HIV, empowerment | 14,634 |
| Households (HR) | Nationwide households: assets, WASH, wealth, infrastructure | 12,949 |
| Children (KR) | Children under 5: nutrition, vaccination, anthropometry, maternal care | 8,092 |
| Summary Stats | National summary indicators with DHS variable codes | 34 indicators |
| Province Table | Key indicators disaggregated by province | 5 provinces + national |
| Edu × Wealth | Cross-tabulation of indicators by education and wealth quintile | 20 rows |

Source: National Institute of Statistics of Rwanda (NISR), Rwanda DHS 2019–20.

## 5. Project Structure

```
rwanda_dhs_dashboard/
├── app.py                  # Main Streamlit application (entry point)
├── style.css                # Full custom enterprise UI styling
├── rwanda.geojson            # Simplified province boundaries for the choropleth map
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .streamlit/
│   └── config.toml           # Streamlit theme & server configuration
├── data/
│   └── rwanda_dhs_2019_20.xlsx   # Source DHS workbook
└── modules/
    ├── __init__.py
    ├── helpers.py             # Data loading, cleaning, formatting utilities
    ├── calculations.py        # All statistical / KPI computation logic
    ├── header.py               # Executive landing header
    ├── footer.py               # Footer with sample sizes & source citation
    ├── filters.py              # Province filter system
    ├── cards.py                 # Five KPI cards
    ├── map.py                    # Interactive choropleth map
    ├── charts.py                 # Full analytics chart suite
    └── tables.py                 # Searchable / sortable / paginated tables
```

## 6. Installation

```bash
git clone <your-repo-url>
cd rwanda_dhs_dashboard
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 7. Running Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## 8. Deployment — Streamlit Community Cloud

1. Push this repository to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select this repository and branch, and set the main file path to `app.py`.
4. Click **Deploy**. Streamlit Cloud will install `requirements.txt` automatically.
5. Confirm the `data/rwanda_dhs_2019_20.xlsx` and `rwanda.geojson` files are committed to the repo (they are required at runtime).

## 9. Screenshots

_Add screenshots of the deployed dashboard here:_

- `docs/screenshot_header.png` — Header and KPI cards
- `docs/screenshot_map.png` — Choropleth map
- `docs/screenshot_analytics.png` — Analytics section
- `docs/screenshot_tables.png` — Data explorer tables

## 10. Dependencies

See `requirements.txt`:

- `streamlit` — application framework
- `pandas` / `numpy` — data processing
- `plotly` — interactive visualizations
- `openpyxl` — Excel file parsing

## 11. Acknowledgements

- **National Institute of Statistics of Rwanda (NISR)** and the **DHS Program** for the underlying survey data.
- Built and maintained by **Faustin NIZEYIMANA**, Statistician and Data Analyst.

## 12. License

This project is provided for educational and analytical demonstration purposes. Underlying DHS microdata usage is subject to the DHS Program's data usage terms. Official published estimates should always be sourced from NISR and the DHS Program.

---

*Interactive dashboard built from Rwanda DHS 2019–20 survey microdata. Results are intended for exploratory analysis and visualization. Official published estimates are available from NISR and the DHS Program.*
