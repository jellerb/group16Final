from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("FIPSAQI.csv")

# print(df)
df["FIPS"]= df["FIPS"].apply(lambda x: '{0:0>5}'.format(x))
# print(df)

import plotly.express as px

fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Median AQI',
                           color_continuous_scale="Viridis",
                           range_color=(0, 90),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'Median AQI':'Average AQI'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()
import plotly.io as pio
pio.write_html(fig, file="index.html", auto_open=True)