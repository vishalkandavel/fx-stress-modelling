import pandas as pd
import matplotlib.pyplot as plt

stress = pd.read_csv(
    "BRICS_Country_FX_Stress_ExpandingCDF.csv",
    index_col=0,
    parse_dates=True
)

ciss = pd.read_csv(
    "BRICS_CISS_FX.csv",
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

colors = {
    "Brazil": "tab:blue",
    "Russia": "tab:red",
    "India": "tab:green",
    "China": "tab:orange",
    "SouthAfrica": "tab:purple"
}

# 1. Country-level FX stress
fig, axes = plt.subplots(5, 1, figsize=(14, 12), sharex=True)

for ax, country in zip(axes, countries):
    ax.plot(
        stress.index,
        stress[country],
        color=colors[country],
        linewidth=0.8
    )
    ax.set_ylabel(country)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)

axes[-1].set_xlabel("Date")
fig.suptitle("BRICS Country-Level FX Stress", fontsize=16)

plt.tight_layout()
plt.savefig("BRICS_Country_FX_Stress.png", dpi=300)
plt.close()


# 2. CISS with financial events
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    ciss.index,
    ciss["Systemic_FX_Stress"],
    color="black",
    linewidth=1.2
)

events = {
    "2007-08-01": "Global Financial Crisis",
    "2008-09-15": "Lehman",
    "2011-08-01": "Eurozone Crisis",
    "2015-08-11": "RMB Devaluation",
    "2020-03-11": "COVID-19",
    "2022-02-24": "Russia-Ukraine"
}

for date, label in events.items():

    date = pd.Timestamp(date)

    if ciss.index.min() <= date <= ciss.index.max():

        ax.axvline(
            date,
            color="tab:red",
            linestyle="--",
            alpha=0.5
        )

        ax.text(
            date,
            0.85,
            label,
            rotation=90,
            verticalalignment="top",
            fontsize=9
        )

ax.set_title("BRICS Systemic FX Stress and Major Financial Events")
ax.set_xlabel("Date")
ax.set_ylabel("Systemic FX Stress")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("BRICS_CISS_FX_Events.png", dpi=300)
plt.close()


# 3. Average country stress vs systemic stress
average_stress = stress[countries].mean(axis=1)

comparison = pd.DataFrame({
    "Average_Country_Stress": average_stress,
    "Systemic_FX_Stress": ciss["Systemic_FX_Stress"]
}).dropna()

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    comparison.index,
    comparison["Average_Country_Stress"],
    color="tab:blue",
    linewidth=1,
    label="Average Country Stress"
)

ax.plot(
    comparison.index,
    comparison["Systemic_FX_Stress"],
    color="tab:red",
    linewidth=1.2,
    label="Systemic FX Stress"
)

ax.set_title("Average Country Stress vs Systemic FX Stress")
ax.set_xlabel("Date")
ax.set_ylabel("Stress")
ax.set_ylim(0, 1)
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("BRICS_Stress_vs_CISS.png", dpi=300)
plt.close()

print("All three graphs saved successfully.")