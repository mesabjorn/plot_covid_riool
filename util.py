# %%
import pandas as pd
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt


def getDateRange(date1, date2):
    results = []

    while(date1 <= date2):
        results.append(date1)
        date1 += timedelta(days=1)
    return results


def interpolate_df(df, col):
    time = df.index
    row = []
    times = []
    for i in range(1, len(time)):
        t0 = time[i-1]
        t1 = time[i]
        b = df[col].iloc[i]
        a = df[col].iloc[i-1]
        delta = df[col].iloc[i]-df[col].iloc[i-1]
        tdelta = (t1-t0).days
        # print(f"delta between {t0} and {t1} = {delta}.")

        interpolated_samples = np.linspace(
            df[col].iloc[i-1], df[col].iloc[i], tdelta+1)

        # interpolated_samples = interpolated_samples[1:-1]
        interpolated_days = getDateRange(t0, t1)
        row = [*row, *interpolated_samples]
        times = [*times, *interpolated_days]
    return pd.DataFrame({"date": times, "value": row})


city = "Ursem"
riool = pd.read_csv("./COVID-19_rioolwaterdata.csv",
                    sep=";", index_col="Date_measurement")

cases = pd.read_csv("./COVID-19_aantallen_gemeente_per_dag.csv",
                    sep=";", index_col="Date_of_publication")

riool.index = pd.to_datetime(riool.index)
cases.index = pd.to_datetime(cases.index)

dfsel = riool.loc[(riool.RWZI_AWZI_name == city)
                  & (riool.index > "2021-01-01")]


# %%
