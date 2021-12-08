import plotly.figure_factory as ff



import pandas as pd
colIn = ["FIPS", "STNAME", "CTYNAME"]
df = pd.read_csv("minoritymajority.csv",
                   usecols= colIn)


# df("STNAME") = df
df["CTYNAME"] = df["CTYNAME"].str.replace(" County", "")
df["CTYNAME"] = df["CTYNAME"].str.replace(" Parish", "")
df["CTYNAME"] = df["CTYNAME"].str.replace(" City", "")
df["CTYNAME"] = df["CTYNAME"].str.replace(" city", "")
df["CTYNAME"] = df["CTYNAME"].str.replace(" Borough", "")

# print(df)
concatStateCity = df.apply(lambda row: row["STNAME"] + row["CTYNAME"], axis = 1)

df["STCITY"] = concatStateCity

# print(df)

# ***********************************************************************************************************
colIn2 = ["State", "County", "Median AQI"]

dfAqi = pd.read_csv("https://raw.githubusercontent.com/jellerb/group16Final/main/PyCharm/FinalProject1/Graphs/annual_aqi_by_county_2021.csv",
                    usecols = colIn2)

dfAqi["County"] = dfAqi["County"].str.replace(" County", "")
dfAqi["County"] = dfAqi["County"].str.replace(" Parish", "")
dfAqi["County"] = dfAqi["County"].str.replace(" City", "")
dfAqi["County"] = dfAqi["County"].str.replace("Saint", "St.")


concatStateCityAqi = dfAqi.apply(lambda row: row["State"] + row["County"], axis = 1)

dfAqi["STCITY"] = concatStateCityAqi

# print(dfAqi)

output1 = pd.merge(df, dfAqi,
                    on = "STCITY",
                   how = "inner"
)


dfFinal = output1[["FIPS", "Median AQI"]]
#
#
print(dfFinal)

dfFinal.to_csv("FIPSAQI.csv", index= False)







