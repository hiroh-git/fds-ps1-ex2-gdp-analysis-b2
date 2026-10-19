from pathlib import Path

import pandas as pd
import wbgapi as wb

# Parameters configuration
COUNTRIES = ["GBR", "USA", "BRA", "JPN", "CHN", "DEU", "CHE"]
START_YEAR = 2000
END_YEAR = 2022
IDs = {
    "real": {"NY.GDP.MKTP.KD": "gdp"},  # Real GDP
    "nominal": {"NY.GDP.MKTP.CD": "gdp"},  # Nominal GDP
}
DATA_DIR = Path(__file__).parent.parent / "data"


# Functions
def load_api_gdp_data(is_real: bool) -> pd.DataFrame:
    """
    Fetches GDP data from the World Bank API for specified countries and years.
    """
    key = "real" if is_real else "nominal"
    indicator = IDs[key]
    df = wb.data.DataFrame(indicator, COUNTRIES, time=range(START_YEAR, END_YEAR))

    df = df.reset_index()

    return df


def load_local_gdp_data(is_real: bool) -> pd.DataFrame:
    """
    Loads GDP data from a local CSV file.
    """
    if is_real:
        gdp_type = "real"
    else:
        gdp_type = "nominal"
    filename = f"gdp_data_{gdp_type}.csv"

    CSV_PATH = DATA_DIR / filename
    df = pd.read_csv(CSV_PATH)

    return df


def save_gdp_data(df: pd.DataFrame, is_real: bool):
    """
    Saves GDP data to a local CSV file.
    """
    if is_real:
        gdp_type = "real"
    else:
        gdp_type = "nominal"
    filename = f"gdp_data_{gdp_type}.csv"
    CSV_PATH = DATA_DIR / filename

    df.to_csv(CSV_PATH, index=False)


def clean_gdp_data(df):
    # Melt
    df_cleaned = df.melt(id_vars=["economy"], var_name="year", value_name="gdp")

    # Rename 'economy' column as 'country'
    df_cleaned = df_cleaned.rename(columns={"economy": "country"})

    # Data types
    df_cleaned["year"] = df_cleaned["year"].str.replace("YR", "").astype(int)
    # df_cleaned['year'] = df_cleaned['year'].astype(int)
    df_cleaned["gdp"] = df_cleaned["gdp"].astype(float)

    # Convert the unit to a trillion US$
    df_cleaned["gdp"] = df_cleaned["gdp"] / 1e12
    df_cleaned = df_cleaned.rename(columns={"gdp": "gdp_t"})

    # Sort by country and year
    df_cleaned = df_cleaned.sort_values(by=["country", "year"])
    df_cleaned = df_cleaned.reset_index(drop=True)
    return df_cleaned
