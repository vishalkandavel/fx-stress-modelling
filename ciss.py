import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stress = pd.read_csv(
    "BRICS_Country_FX_Stress_ExpandingCDF.csv",
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

stress = stress[countries].dropna()

# 60-day rolling correlations
correlations = stress.rolling(60).corr()

# Equal country weights
weights = np.ones(5) / 5

systemic_stress = pd.Series(
    index=stress.index,
    dtype=float
)

for date in stress.index:

    try:
        corr_matrix = correlations.loc[date].values

        if np.isnan(corr_matrix).any():
            continue

        stress_vector = stress.loc[date].values
        weighted_stress = weights * stress_vector

        systemic_stress.loc[date] = (
            weighted_stress @
            corr_matrix @
            weighted_stress
        )

    except (KeyError, ValueError):
        continue

systemic_stress = systemic_stress.dropna()

result = pd.DataFrame({
    "Brazil_FX_Stress": stress.loc[systemic_stress.index, "Brazil"],
    "Russia_FX_Stress": stress.loc[systemic_stress.index, "Russia"],
    "India_FX_Stress": stress.loc[systemic_stress.index, "India"],
    "China_FX_Stress": stress.loc[systemic_stress.index, "China"],
    "SouthAfrica_FX_Stress": stress.loc[systemic_stress.index, "SouthAfrica"],
    "Systemic_FX_Stress": systemic_stress
})

result.to_csv("BRICS_CISS_FX.csv")

print(result.head())
print(result.tail())
print(result.describe())

plt.figure(figsize=(14, 6))
plt.plot(
    result.index,
    result["Systemic_FX_Stress"]
)

plt.title("BRICS Systemic FX Stress Index")
plt.xlabel("Date")
plt.ylabel("Systemic FX Stress")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "BRICS_CISS_FX.png",
    dpi=300
)

plt.show()