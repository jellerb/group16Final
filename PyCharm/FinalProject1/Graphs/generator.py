import pandas as pd
from pandas.core.frame import DataFrame
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px
import csv

datavar = "annual_aqi_by_county_2021.csv"
yearvar = "US_Average_AQI.csv"

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
    #Define variables
    states = {}
    data_doc = open(dataset, 'r')
    data = csv.reader(data_doc)#, delimiter=' ', quotechar='"')

    #Iterate through the CSV file and make a dictionary storing the counties by state.
    #Example: {"North Carolina": ["Mecklenburg", "Orange", "Wake", "Cabarrus"]}
    for row in data:
        if row[0] not in states:
            states[row[0]] = [row[1]]
        else:
            temp = states[row[0]]
            temp.append(row[1])
            states[row[0]] = temp

    #Iterate through the dict of states and grab the counties in each state.
    for state in states:
        data_doc.seek(0)
        display_data = {}

        #Read through the csv file row by row and check it against the current state
        for row in data:
            print(row)
            if row[0] == state or row[0] == "State":
                append_list = row[2:]
                final_list = []

                #Convert all integer compatible values, i.e. "0", to integers.
                #Fixes error with stacked graph displaying incorrectly.
                for item in append_list:
                    try:
                        final_list.append(int(item))
                    except:
                        final_list.append(item)
                display_data[row[1]] = final_list
        
        #The way that the dict is written includes the header, this if statement will make it skip the header and only the header.
        if (len(display_data.keys()) > 1):
            df = DataFrame.from_dict(display_data, orient='index').reset_index()
            column_array = ['County',]

            #Create the header data for the dataframe.
            for item in display_data['County']:
                column_array.append(item)

            #Add the ehader data, drop the header which was taken as data, and reset the index.
            df.set_axis(column_array, axis=1, inplace=True)
            df = df.drop(0)
            df.reset_index()
            print("\n\n\n")
            print(df)

            #Create a new dataframe for display which has the pertinent information.
            new_df = df.groupby(['County']).agg({
                'Good Days': 'sum',
                'Moderate Days': 'sum',
                'Unhealthy Days': 'sum',
                'Unhealthy for Sensitive Groups Days': 'sum',
                'Very Unhealthy Days': 'sum',
                'Hazardous Days': 'sum',
                'Days with AQI': 'sum'
                }).reset_index()

            #Sort the new dataframe by the amount of data, low to high.
            new_df = new_df.sort_values(by=['Days with AQI'], ascending=[True])
            print(new_df)
            
            #"Good Days","Moderate Days","Unhealthy for Sensitive Groups Days","Unhealthy Days","Very Unhealthy Days","Hazardous Days"
            #This creates the different bars for the stacked bar chart to use.
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

    #Close the reader.
    data_doc.close()

def generateByYearGraphs(dataset):
    data_dict = {}
    data_doc = open(dataset, 'r')
    data = csv.reader(data_doc)

    #Parse data into dict
    for row in data:
        data_dict[int(row[0])] = float(row[1])

    #Create Data Frame and prepare to make graph.
    df = DataFrame.from_dict(data_dict, orient='index').reset_index()
    df.rename(columns={'index': 'year', 0: 'AQI'}, inplace=True)
    print(df)

    #Generate the graph
    fig = px.line(df, x="year", y="AQI", title='AQI Per Year Since 1980')
    #fig.show()
    file_name = "graphs/yearlyAQI.html"
    pyo.plot(fig, filename=file_name)

def generatePieGraph(dataset):
    data_dict = {}
    data_doc = open(dataset, 'r')
    data = csv.reader(data_doc)

    #Parse data into dict
    for row in data:
        data_dict[row[0]] = row[1:]

    #Create Data Frame and prepare to make graph.
    df = DataFrame.from_dict(data_dict, orient='index').reset_index()

    column_array = ['State',]

    #Create the header data for the dataframe.
    for item in data_dict['State']:
        column_array.append(item)

    #Purge the incorrectly parsed line and add the correct headers to the dataframe.
    df.set_axis(column_array, axis=1, inplace=True)
    df = df.drop(0)
    df.reset_index()
    print(df)
    
    #Tries to turn every value in the dataframe into a float, passes over the ones it fails.
    #This is done because when the dict was created, all values parsed from the csv were strings.
    df = df.apply(pd.to_numeric, errors='ignore')

    #Create a new dictionary using the dataset, this will be used to generate the final dataset.
    data_set = {
        'Good Days': sum(df['Good Days']),
        'Moderate Days': sum(df['Moderate Days']),
        'Unhealthy for Sensitive Groups Days': sum(df['Unhealthy for Sensitive Groups Days']),
        'Unhealthy Days': sum(df['Unhealthy Days']),
        'Very Unhealthy Days': sum(df['Very Unhealthy Days']),
        'Hazardous Days': sum(df['Hazardous Days'])
    }

    #Convert the dictionary into a dataframe for the graph generation.
    new_df = DataFrame.from_dict(data_set, orient='index').reset_index()

    #Generate the pie chart.
    fig = px.pie(new_df, values=0, names='index', title='AQI In the United States in 2021')
    #fig.show()
    file_name = "graphs/USAPieChart.html"
    pyo.plot(fig, filename=file_name)

generateCountyGraphs(datavar)
generateStatesGraph(datavar)
generateByYearGraphs(yearvar)
generatePieGraph(datavar)