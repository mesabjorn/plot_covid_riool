# %%
#
import pandas as pd
import sys
import matplotlib.pyplot as plt
from util import interpolate_df


def performcorrelationanalysis(df):
    f, ax = plt.subplots(5, 3, figsize=(10, 15))
    f2, ax2 = plt.subplots(5, 3, figsize=(10, 15))
    curax = 0
    for d in range(0, 15):
        shifted = df.Total_reported.shift(-1*d)
        val = df.value/df.value.max()
        shifted = shifted/shifted.max()
        row = curax//3
        col = curax % 3
        # print({"row": row, "col": col})
        ax[row, col].plot(df.index, val,
                          'o-', label="value")
        ax[row, col].plot(df.index, shifted,
                          'o-', label="shifted")
        ax[row, col].set_title(f"shift:{d}")

        ax2[row, col].plot(val, shifted /
                           shifted.max(), 'o')
        ax2[row, col].set_title(f"shift:{d}")

        c = val.corr(shifted)
        # print(f"corr for shift {d*-1} is {c}")
        ax2[row, col].text(0.1, .9, f"{c: 0.3f}")
        curax += 1
    plt.show()


def load_csv(city):
    riool = pd.read_csv("./COVID-19_rioolwaterdata.csv",
                        sep=";", index_col="Date_measurement")

    cases = pd.read_csv("./COVID-19_aantallen_gemeente_per_dag.csv",
                        sep=";", index_col="Date_of_publication")

    riool.index = pd.to_datetime(riool.index)
    cases.index = pd.to_datetime(cases.index)

    dfsel = riool.loc[(riool.RWZI_AWZI_name == city)
                      & (riool.index > "2021-01-01")]

    riooli = interpolate_df(dfsel, "RNA_flow_per_100000")

    casessel = cases.loc[(cases.Municipality_name == 'Medemblik') & (
        cases.index > "2021-01-01")]

    riooli = interpolate_df(dfsel, "RNA_flow_per_100000")
    riooli = riooli.set_index("date")
    riooli.index = pd.to_datetime(riooli.index)
    riooli = riooli.join(casessel.Total_reported)

    f, ax = plt.subplots(2, 1, figsize=(10, 7))

    ax[0].plot(riooli.index, riooli.value,
               'o-', label="RNA flow per 100000")
    # plt.xticks(rotation=30, ha="right")
    ax[0].set_ylabel("RNA flow per 100000")
    ax[0].set_title(city)

    ax[1].plot(riooli.index, riooli.Total_reported,
               'o-', label="Total_reported")
    # plt.xticks(rotation=30, ha="right")
    ax[1].set_ylabel("Total_reported")
    ax[1].set_title(city)
    plt.show()

    performcorrelationanalysis(riooli)


if __name__ == "__main__":
    if(len(sys.argv) == 2):
        city = sys.argv[1]
    else:
        city = "Ursem"
    load_csv(city)
