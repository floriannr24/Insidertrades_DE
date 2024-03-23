import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from statsmodels.graphics.correlation import plot_corr
import statsmodels.graphics.correlation as corr
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

df = pd.read_excel("C:/Users/FSX-P/Insider_DE-df.xlsx")

df_new = df
df_new["isVorstand"] = df["Position / Status"].apply(lambda x: 1 if x == "Vorstand" else 0)
df_new["%5"] = df_new["%5"].apply(lambda x: x*100)
df_new["%10"] = df_new["%10"].apply(lambda x: x*100)
df_new["%20"] = df_new["%20"].apply(lambda x: x*100)
df_new["%30"] = df_new["%30"].apply(lambda x: x*100)
df_new = df_new[df_new["Code"] != "DB1.DE"]

df_new["over500k"] = df_new["Aggregiertes Volumen"].apply(lambda x: 1 if x >= 500000 else 0)
df_new["avg"] = df_new[["%5", "%10", "%20", "%30"]].mean(axis=1)

# counts = df_new["Code"].value_counts()
# df_new = df_new[df_new["Code"].isin(counts[counts > 2].index)]
# df_new = df[df["Aggregiertes Volumen"] > 100000]

df_new = df_new.dropna()
pd.set_option('display.max_columns', None)

# df_to_std = df_new.copy()[["Aggregiertes Volumen", "%5", "%10", "%20", "%30"]]
#
# # scaler = StandardScaler()
# # scaler.fit(df_to_std)
# # df_std_new = scaler.transform(df_to_std)
# # df_std = pd.DataFrame(df_std_new)

# model = LinearRegression()
# model.fit(df_new[["isVorstand", "Aggregiertes Volumen"]], df_new["avg"])
#
# print(model.score(df_new[["isVorstand", "Aggregiertes Volumen"]], df_new["avg"]))

x = "Aggregiertes Volumen"
y = "avg"

sns.scatterplot(x=x, y=y, data=df_new)
sns.regplot(x=x, y=y, data=df_new)

plt.show()