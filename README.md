# Montreal Food Inspection Violations Analysis

Data analysis project exploring food safety violations in Montreal using open data from the City of Montreal.

## Key Findings

- **Top offenders**: Identifies establishments with the most repeat violations
- **Trends over time**: Year-over-year violation patterns reveal enforcement cycles
- **Fine distribution**: Analysis of penalty amounts across violation categories
- **Geographic hotspots**: Boroughs with highest violation density

## Tech Stack

- **Python 3** - Core language
- **pandas** - Data manipulation and cleaning
- **matplotlib** - Static visualizations
- **seaborn** - Statistical visualization
- **requests** - Data fetching from Montreal Open Data API

## Visualizations

| Chart | Description |
|-------|-------------|
| Top 20 Establishments | Horizontal bar chart of most-cited businesses |
| Yearly Trends | Line chart showing violations over time |
| Fine Distribution | Histogram of penalty amounts |
| Top Boroughs | Bar chart of violations by city/borough |
| Status Breakdown | Pie chart of violation outcomes |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python3 analysis.py
```

Charts are saved to the `output/` directory.

## Data Source

[City of Montreal Open Data - Food Inspection Violations](https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0)
