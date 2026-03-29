"""
Montreal Food Inspection Violations - Data Analysis
Explores trends, repeat offenders, and fine distributions
using open data from the City of Montreal.
"""

import os
import requests
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Data source
URL = (
    "https://data.montreal.ca/dataset/"
    "05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/"
    "7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"
)

OUTPUT_DIR = "output"

# Visual style
sns.set_theme(style="darkgrid")
PALETTE = ["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe"]
plt.rcParams.update({
    "figure.figsize": (12, 6),
    "figure.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
})


def download_data():
    """Download violations CSV from Montreal Open Data."""
    print("Downloading data from Montreal Open Data...")
    response = requests.get(URL, timeout=30)
    response.encoding = "utf-8"
    df = pd.read_csv(io.StringIO(response.text))
    print(f"Downloaded {len(df)} records.")
    return df


def parse_date_col(series):
    """Parse date columns from YYYYMMDD integer format."""
    return pd.to_datetime(series, format="%Y%m%d", errors="coerce")


def clean_data(df):
    """Clean and prepare the dataset."""
    print("Cleaning data...")

    # Parse dates
    df["date"] = parse_date_col(df["date"])
    df["date_jugement"] = parse_date_col(df["date_jugement"])
    df["date_statut"] = parse_date_col(df["date_statut"])

    # Clean monetary amounts
    df["montant"] = pd.to_numeric(df["montant"], errors="coerce")

    # Extract year for trend analysis
    df["year"] = df["date"].dt.year

    # Normalize city names (trim whitespace, title case)
    df["ville"] = df["ville"].str.strip().str.title()

    # Drop rows with no valid date
    df = df.dropna(subset=["date"])

    print(f"Cleaned dataset: {len(df)} records.")
    return df


def print_summary(df):
    """Print key statistics to console."""
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total violations:        {len(df):,}")
    print(f"Unique establishments:   {df['etablissement'].nunique():,}")
    print(f"Date range:              {df['date'].min():%Y-%m-%d} to "
          f"{df['date'].max():%Y-%m-%d}")
    print(f"Average fine:            ${df['montant'].mean():,.0f}")
    print(f"Median fine:             ${df['montant'].median():,.0f}")
    print(f"Total fines collected:   ${df['montant'].sum():,.0f}")
    print(f"Cities/Boroughs:         {df['ville'].nunique()}")
    print("=" * 60)


def plot_top_establishments(df):
    """Top 20 establishments with most violations."""
    top = (df.groupby("etablissement")
             .size()
             .sort_values(ascending=False)
             .head(20)
             .sort_values())

    fig, ax = plt.subplots(figsize=(12, 8))
    top.plot(kind="barh", ax=ax, color="#2563eb", edgecolor="white")
    ax.set_title("Top 20 Establishments with Most Violations")
    ax.set_xlabel("Number of Violations")
    ax.set_ylabel("")
    ax.tick_params(axis="y", labelsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_establishments.png"))
    plt.close()
    print("  Saved: top_establishments.png")


def plot_yearly_trends(df):
    """Violations per year trend line."""
    yearly = (df.groupby("year")
                .size()
                .reset_index(name="count"))

    # Filter out incomplete years
    current_year = datetime.now().year
    yearly = yearly[(yearly["year"] >= 2000) &
                    (yearly["year"] <= current_year)]

    fig, ax = plt.subplots()
    ax.plot(yearly["year"], yearly["count"],
            marker="o", color="#2563eb", linewidth=2.5,
            markersize=6, markerfacecolor="white",
            markeredgewidth=2, markeredgecolor="#2563eb")
    ax.fill_between(yearly["year"], yearly["count"],
                    alpha=0.1, color="#2563eb")
    ax.set_title("Food Violations Over Time (by Year)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Violations")
    ax.set_xticks(yearly["year"][::2])
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "yearly_trends.png"))
    plt.close()
    print("  Saved: yearly_trends.png")


def plot_fine_distribution(df):
    """Distribution of fine amounts."""
    fines = df["montant"].dropna()
    fines = fines[(fines > 0) & (fines < fines.quantile(0.99))]

    fig, ax = plt.subplots()
    sns.histplot(fines, bins=40, color="#2563eb", edgecolor="white",
                 alpha=0.8, ax=ax)
    ax.axvline(fines.median(), color="#ef4444", linestyle="--",
               linewidth=2, label=f"Median: ${fines.median():,.0f}")
    ax.axvline(fines.mean(), color="#f59e0b", linestyle="--",
               linewidth=2, label=f"Mean: ${fines.mean():,.0f}")
    ax.legend()
    ax.set_title("Distribution of Fine Amounts")
    ax.set_xlabel("Fine Amount ($)")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fine_distribution.png"))
    plt.close()
    print("  Saved: fine_distribution.png")


def plot_top_cities(df):
    """Top 10 cities/boroughs by violation count."""
    top = (df.groupby("ville")
             .size()
             .sort_values(ascending=False)
             .head(10))

    fig, ax = plt.subplots()
    sns.barplot(x=top.values, y=top.index, ax=ax,
                palette="Blues_r", edgecolor="white")
    ax.set_title("Top 10 Cities / Boroughs by Violations")
    ax.set_xlabel("Number of Violations")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_cities.png"))
    plt.close()
    print("  Saved: top_cities.png")


def plot_status_breakdown(df):
    """Pie chart of violation statuses."""
    status = df["statut"].value_counts().head(6)

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = sns.color_palette("Blues_r", n_colors=len(status))
    wedges, texts, autotexts = ax.pie(
        status.values,
        labels=status.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        pctdistance=0.85,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for text in autotexts:
        text.set_fontsize(10)
        text.set_fontweight("bold")
    ax.set_title("Violation Status Breakdown")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "status_breakdown.png"))
    plt.close()
    print("  Saved: status_breakdown.png")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = download_data()
    df = clean_data(df)
    print_summary(df)

    print("\nGenerating visualizations...")
    plot_top_establishments(df)
    plot_yearly_trends(df)
    plot_fine_distribution(df)
    plot_top_cities(df)
    plot_status_breakdown(df)

    print(f"\nAll charts saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
