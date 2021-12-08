import pandas as pd

colIn = ["code", "state"]
df = pd.read_csv("2011_us_ag_exports.csv",
                    usecols = colIn)

# print(df)

colIn2 = ["State", "Median AQI"]

dfAqi = pd.read_csv("https://raw.githubusercontent.com/jellerb/group16Final/main/PyCharm/FinalProject1/Graphs/annual_aqi_by_county_2021.csv",
                    usecols = colIn2)

# print(dfAqi)

dfAvg = dfAqi.groupby("State", as_index= False)["Median AQI"].mean()

dfAvg = dfAvg.rename(str.lower, axis = 'columns')

# print(dfAvg)

dfCodeAqi = pd.merge(df, dfAvg,
                    on = "state",
                   how = "inner"
)

print(dfCodeAqi)

dfCodeAqi.to_csv("CODEAQI.csv", index= False)