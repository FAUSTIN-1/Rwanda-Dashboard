# 🇷🇼 Rwanda DHS 2019–20 Dashboard

## National Health and Demographic Intelligence

This project is an interactive Streamlit dashboard built using the Rwanda Demographic and Health Survey (DHS) 2019–20 microdata. It allows users to explore key health and demographic indicators through interactive charts, maps, and tables. The dashboard was developed as a portfolio project to demonstrate practical skills in statistics, data analysis, public health analytics, geospatial visualization, and dashboard development.

**Author:** Faustin NIZEYIMANA  
**Role:** Statistician & Data Analyst

---

# Project Overview

The Rwanda DHS 2019–20 Dashboard brings together data from the Women, Household, and Children survey datasets into a single interactive application. Instead of relying on static reports, users can filter the data by province, explore demographic and health indicators, and visualize results through interactive charts and maps.

The dashboard covers a wide range of topics including fertility, family planning, maternal and child health, HIV testing, nutrition, education, household characteristics, and wealth indicators. All statistics displayed in the dashboard are calculated directly from the survey microdata.

---

# Why I Built This Project

I built this dashboard to strengthen my practical skills in statistical analysis, data visualization, and interactive dashboard development using real-world survey data.

The Rwanda DHS dataset contains valuable information for understanding population health and socioeconomic conditions. This project demonstrates how survey microdata can be transformed into an accessible and interactive decision-support tool for researchers, students, policymakers, and anyone interested in exploring Rwanda's health and demographic indicators.

---

# Project Objectives

The main objectives of this project are to:

- Present Rwanda DHS 2019–20 indicators in an interactive and easy-to-understand format.
- Allow users to compare indicators across Rwanda's five provinces.
- Replace static tables with dynamic visualizations and filters.
- Demonstrate practical applications of statistics, public health analytics, and dashboard development using Python and Streamlit.

---

# Dashboard Features

The dashboard includes several interactive components designed to make exploring DHS data easier.

### Executive Dashboard

- Professional landing page
- Responsive layout
- Clean custom interface built with Streamlit and CSS

### Key Performance Indicators

Five summary indicators are displayed at the top of the dashboard:

- Family Planning
- Child Nutrition
- HIV Testing
- Health Insurance
- Fertility

Each KPI updates automatically when a province is selected.

### Province Filter

Users can explore results for:

- National
- Kigali City
- Southern Province
- Eastern Province
- Northern Province
- Western Province

All charts, maps, and summary indicators update based on the selected province.

### Interactive Rwanda Map

The dashboard includes a choropleth map of Rwanda built using a GeoJSON file.

Users can switch between several indicators, including:

- Modern Contraceptive Prevalence
- Child Stunting
- Health Insurance Coverage
- HIV Testing
- Fertility Rate
- Skilled Antenatal Care

Hovering over a province displays additional information such as indicator values and sample sizes.

### Data Visualizations

The dashboard contains more than fifteen interactive visualizations, including:

- Population pyramid
- Age distribution
- Fertility analysis
- Maternal care cascade
- Family planning analysis
- Child nutrition indicators
- Wealth distribution
- Education and wealth heatmap
- Household infrastructure indicators
- Province comparisons
- Lollipop chart
- Radar chart
- Donut charts
- Treemap
- Funnel chart
- Slope chart
- Ranked horizontal bar chart

### Data Explorer

The dashboard also includes searchable and sortable tables for:

- Women dataset
- Household dataset
- Children dataset

Filtered data can be downloaded as CSV files.

---

# Dataset

The dashboard is built from a cleaned Excel workbook containing Rwanda DHS 2019–20 survey microdata.

| Dataset | Description | Records |
|----------|-------------|--------:|
| Women (IR) | Women aged 15–49 including fertility, family planning, HIV, maternal health, and related indicators | 14,634 |
| Households (HR) | Household characteristics, assets, sanitation, water, wealth, and infrastructure | 12,949 |
| Children (KR) | Children under five including nutrition, vaccination, anthropometry, and maternal care | 8,092 |
| Summary Statistics | National indicators with DHS variable references | 34 |
| Province Table | Province-level indicators | 5 Provinces + National |
| Education × Wealth | Cross-tabulation by education and wealth quintile | 20 Rows |

**Source:** National Institute of Statistics of Rwanda (NISR) and the DHS Program.

---

# Project Structure

```text
rwanda_dhs_dashboard/
│
├── app.py
├── style.css
├── requirements.txt
├── README.md
├── rwanda.geojson
│
├── data/
│   └── rwanda_dhs_2019_20.xlsx
│
├── modules/
│   ├── calculations.py
│   ├── cards.py
│   ├── charts.py
│   ├── filters.py
│   ├── footer.py
│   ├── header.py
│   ├── helpers.py
│   ├── map.py
│   └── tables.py
│
└── .streamlit/
    └── config.toml
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/your-username/rwanda-dhs-dashboard.git
```

Move into the project folder.

```bash
cd rwanda-dhs-dashboard
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the virtual environment.

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

---

# Run the Application

Start the Streamlit application.

```bash
streamlit run app.py
```

The dashboard will open in your browser at:

```
http://localhost:8501
```

---

# Deployment

This project can be deployed directly to Streamlit Community Cloud.

1. Push the repository to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Create a new application.
4. Select this repository.
5. Choose `app.py` as the entry point.
6. Deploy the application.

Make sure both the dataset and `rwanda.geojson` file are included in the repository.

---

# Screenshots

You can add screenshots of the dashboard here after deployment.

- Dashboard Home
- KPI Cards
- Rwanda Choropleth Map
- Analytics Section
- Data Tables

---

# Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- OpenPyXL

---

# Acknowledgements

I would like to acknowledge the National Institute of Statistics of Rwanda (NISR) and the DHS Program for providing access to the Rwanda DHS 2019–20 survey data.

---

# License

This project was developed for educational purposes and as part of my professional data analytics portfolio.

The underlying DHS microdata remain subject to the data usage policies of the DHS Program. Official published estimates should always be obtained from NISR and the DHS Program.

---

> **Note:** This dashboard is intended for exploratory analysis and visualization. It should not be considered a replacement for official DHS reports or published estimates.
