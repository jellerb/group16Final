import plotly.graph_objects as go

import pandas as pd
df = pd.read_csv('CODEAQI.csv')

fig = go.Figure(data=go.Choropleth(
    locations=df['code'], # Spatial coordinates
    z = df['median aqi'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'blues',
    colorbar_title = "Average AQ",
))

fig.update_layout(
    title_text = 'Average Air Quality Index By State',
    geo_scope='usa', # limite map scope to USA
)

import plotly.io as pio
pio.write_html(fig, file="StateAqiMap.html", auto_open=True)