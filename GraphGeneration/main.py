import pandas as pd
from pandas.core.frame import DataFrame
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px
import csv
import numpy as np

datavar = "annual_aqi_by_county_2021.csv"

def generateStatesGraph(dataset):
    # Load CSV file from Datasets folder
    df = pd.read_csv(dataset)

    # Creating sum of number of cases group by Country Column
    new_df = df.groupby(['State']).agg({
        'Median AQI': 'mean', 
        'Good Days': 'sum',
        'Unhealthy Days': 'sum',
        'Hazardous Days': 'sum'
        }).reset_index()

    #Remove Mexico from Consideration:
    new_df = new_df.drop(7)

    # Sorting values and select 20 first value
    new_df = new_df.sort_values(by=['Median AQI'], ascending=[True])

    print(new_df)

    # Preparing data
    trace1 = go.Bar(x=new_df['State'], y=new_df['Median AQI'], name='Average AQI', marker={'color': '#0000FF'})
    #trace2 = go.Bar(x=new_df['State'], y=new_df['Unhealthy Days'], name='Unhealthy', marker={'color': '#9EA0A1'})
    #trace3 = go.Bar(x=new_df['State'], y=new_df['Hazardous Days'], name='Hazardous', marker={'color': '#FFD700'})
    data = [trace1]

    # Preparing layout
    layout = go.Layout(title='AQI Sorted by State', xaxis_title="State",
                    yaxis_title="Average AQI (Higher is Worse)", barmode='stack')

    # Plot the figure and saving in a html file
    fig = go.Figure(data=data, layout=layout)
    file_name = "graphs/stateAQI.html"
    pyo.plot(fig, filename=file_name)

def generateCountyGraphs(dataset):
    states = {}
    data_doc = open(dataset, 'r')
    data = csv.reader(data_doc)#, delimiter=' ', quotechar='"')

    for row in data:
        if row[0] not in states:
            states[row[0]] = [row[1]]
        else:
            temp = states[row[0]]
            temp.append(row[1])
            states[row[0]] = temp

    for state in states:
        data_doc.seek(0)
        display_data = {}

        for row in data:
            print(row)
            if row[0] == state and row[0] != "State":
                converted = row[3:]
                new_conv = [row[2],]
                for number in converted:
                    new_conv.append(int(number))
                display_data[row[1]] = new_conv
            if row[0] == "State":
                display_data[row[1]] = row[2:]
   

        print(display_data)
        if (len(display_data.keys()) > 1):
            df = DataFrame.from_dict(display_data, orient='index').reset_index()
            column_array = ['County',]

            for item in display_data['County']:
                column_array.append(item)

            df.set_axis(column_array, axis=1, inplace=True)
            df = df.drop(0)
            df.reset_index()

            print("\n\n\n")
            print(df)

            new_df = df.groupby(['County']).agg({
                'Good Days': 'sum',
                'Moderate Days': 'sum',
                'Unhealthy Days': 'sum',
                'Unhealthy for Sensitive Groups Days': 'sum',
                'Very Unhealthy Days': 'sum',
                'Hazardous Days': 'sum',
                'Days with AQI': 'sum'
                }).reset_index()

            new_df = new_df.sort_values(by=['Days with AQI'], ascending=[True])
            #new_df[2:] = new_df[2:].apply(pd.to_numeric)
            print(new_df)
            
            #"Good Days","Moderate Days","Unhealthy for Sensitive Groups Days","Unhealthy Days","Very Unhealthy Days","Hazardous Days"
            trace1 = go.Bar(x=new_df['County'], y=new_df['Good Days'], name='Good Days', marker={'color': '#00FF00'})
            trace2 = go.Bar(x=new_df['County'], y=new_df['Moderate Days'], name='Moderate Days', marker={'color': '#FFFF00'})
            trace3 = go.Bar(x=new_df['County'], y=new_df['Unhealthy for Sensitive Groups Days'], name='Unhealthy for Sensitive Groups', marker={'color': '#FFA500'})
            trace4 = go.Bar(x=new_df['County'], y=new_df['Unhealthy Days'], name='Unhealthy Days', marker={'color': '#FF0000'})
            trace5 = go.Bar(x=new_df['County'], y=new_df['Very Unhealthy Days'], name='Very Unhealthy Days', marker={'color': '#8B0000'})
            trace6 = go.Bar(x=new_df['County'], y=new_df['Hazardous Days'], name='Hazardous Days', marker={'color': '#000000'})

            output_data = [trace1, trace2, trace3, trace4, trace5, trace6]

            # Preparing layout
            title_string = "AQI Sorted by County in " + state
            layout = go.Layout(title=title_string, xaxis_title="County", yaxis_title="Days Polled", barmode='stack')

            # Plot the figure and saving in a html file

            fig = go.Figure(data=output_data, layout=layout)
            file_name = "graphs/" + state + "CountyAQI.html"
            pyo.plot(fig, filename=file_name)

    data_doc.close()

generateCountyGraphs(datavar)
generateStatesGraph(datavar)