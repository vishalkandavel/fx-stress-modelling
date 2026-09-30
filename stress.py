import pandas as pd
import numpy as np

fx = pd.read_csv(
    "BRICS_FX_Raw_Data.csv",
    index_col=0,
    parse_dates=True
)

countries = [
    "Brazil",
    "Russia",
    "India",
    "China",
    "SouthAfrica"
]

fx = fx[countries].dropna()

returns = np.log(fx / fx.shift(1))
abs_returns = returns.abs()

volatility = returns.rolling(20).std()

rolling_min = fx.rolling(21).min()
depreciation_stress = fx / rolling_min - 1


def expanding_cdf(series):
    result = pd.Series(index=series.index, dtype=float)
    history = []

    for date in series.index:
        value = series.loc[date]

        if pd.isna(value):
            continue

        history.append(value)
        result.loc[date] = np.mean(np.array(history) <= value)

    return result


cdf_returns = abs_returns.apply(expanding_cdf)
cdf_volatility = volatility.apply(expanding_cdf)
cdf_depreciation = depreciation_stress.apply(expanding_cdf)

country_stress = (
    cdf_returns +
    cdf_volatility +
    cdf_depreciation
) / 3

country_stress = country_stress.dropna()

stress_scores = pd.DataFrame(index=country_stress.index)

for country in countries:

    stress_scores[f"{country}_Abs_Return"] = abs_returns[country]
    stress_scores[f"{country}_Volatility"] = volatility[country]
    stress_scores[f"{country}_Depreciation"] = depreciation_stress[country]

    stress_scores[f"{country}_Return_CDF"] = cdf_returns[country]
    stress_scores[f"{country}_Volatility_CDF"] = cdf_volatility[country]
    stress_scores[f"{country}_Depreciation_CDF"] = cdf_depreciation[country]

    stress_scores[f"{country}_FX_Stress"] = country_stress[country]

stress_scores.to_csv(
    "BRICS_FX_Stress_Scores_ExpandingCDF.csv"
)

country_stress.to_csv(
    "BRICS_Country_FX_Stress_ExpandingCDF.csv"
)

print(country_stress.head())
print(country_stress.tail())
print(country_stress.describe())

print("\nSaved:")
print("BRICS_FX_Stress_Scores_ExpandingCDF.csv")
print("BRICS_Country_FX_Stress_ExpandingCDF.csv")