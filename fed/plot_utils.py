import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import ticker


def plot_gdp_trends(df: pd.DataFrame, is_real: bool):
    """
    Plots the GDP data.
    """
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # Plot line graph
    sns.lineplot(data=df, x="year", y="gdp_t", hue="country")

    # Set the x-axis scale to 5-year intervals
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))

    # Labels and a title
    gdp_type = "Real" if is_real else "Nominal"
    plt.title(
        f"{gdp_type} GDP Trend by Country (Trillion US$)",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("GDP", fontsize=12)

    # Legends
    plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    plt.show()
