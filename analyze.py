import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
from statsmodels.graphics.correlation import plot_corr
import statsmodels.graphics.correlation as corr
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("C:/Users/FSX-P/Insider_DE-df.xlsx")

df_new = df
df_new["isVorstand"] = df["Position / Status"].apply(lambda x: 1 if x == "Vorstand" else 0)
df_new["%5"] = df_new["%5"].apply(lambda x: x*100)
df_new["%10"] = df_new["%10"].apply(lambda x: x*100)
df_new["%20"] = df_new["%20"].apply(lambda x: x*100)
df_new["%30"] = df_new["%30"].apply(lambda x: x*100)
# df_new = df[df["Emittent"] != "Deutsche Börse Aktiengesellschaft"]
# df_new = df[df["Aggregiertes Volumen"] > 500000]
# df["over200k"] = df["Aggregiertes Volumen"].apply(lambda x: 1 if x >= 200000 else 0)
# df["under200k"] = df["Aggregiertes Volumen"].apply(lambda x: 1 if x < 200000 else 0)

df_new = df_new[["isVorstand", "Aggregiertes Volumen", "%5", "%10", "%20", "%30"]]
df_new = df_new.dropna()

df_std = df_new

scaler = StandardScaler()
scaler.fit(df_std)
df_std_new = scaler.transform(df_std)
df_std_new = pd.DataFrame(df_std_new)

corrMatrix = df_std_new.corr(method="pearson")
sns.heatmap(corrMatrix, annot=True, cmap="Greens", xticklabels=df_new.columns, yticklabels=df_new.columns)
plt.tight_layout()
plt.show()