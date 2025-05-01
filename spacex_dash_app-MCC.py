# Import required libraries 
# (dash not initially installed!!!): >> python -m pip install dash 

# To run the code:
#   Open a new terminal
#   Move to the proper folder
#   Write the command '> python '.space_dash-MCC.py'
#   Press ENTER
#   Ctrl+Click on the URL (e.g. http://127.0.0.1:8050)

import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
 
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
 
# Create a dash application
app = dash.Dash(__name__)
 
# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
             style={'textAlign': 'center', 
                    'color': 'darkblue', 
                    'font-size': '72px',
                    'font-weight': 'bolder',
                    'font-family': 'Helvetica',
                    'padding': '20px',
                    'transform': 'perspective(500px) rotateX(15deg)'}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'},
                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
        value='ALL',
        placeholder="Place holder site here",
        searchable=True,
        clearable=False,
        style={'fontFamily': 'Helvetica', 
               'fontSize': '20px',                
               'color': 'darkblue',              
               'borderRadius': '4px',             
               'width': '38%'}),
    html.Br(),
 
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
 
    html.P("Payload range (kg):",
           style={'fontFamily': 'Helvetica',  
                  'fontSize': '20px',                
                  'color': 'darkblue', 
                  'fontWeight': 'bold',              
                  'margin': '10px 0'}),
    dcc.RangeSlider(id='payload-slider',
                    min=0, 
                    max=10_000, 
                    step=1_000,
                    marks = {i: {'label': f'{i:,}', 'style': {'fontSize': '18px'}} for i in range(0, 10_001, 1_000)},
                    value=[min_payload, max_payload]),
 
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Br(),
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))])
 
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, 
                     values='class', 
                     names='Launch Site', 
                     title='<b>Total Successful Launches by Site.</b>')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class_count')
        filtered_df['class_name'] = filtered_df['class'].map({0: 'Failure', 1: 'Success'})
        fig = px.pie(filtered_df, 
                     values='class_count', 
                     names='class_name',
                     title=f'<b>Total Sucessful Launches for Site {entered_site}.</b>')
    
    fig.update_traces(textfont_size=14,
                      textinfo='percent',
                      insidetextorientation='horizontal',
                      marker={'line': {'color': 'white', 'width':2}})
    
    fig.update_layout(legend={'font': {'size':16}, 'bgcolor': 'lightgrey', 'x': 0.70, 'y': 0.90},
                      title_font={'size':22}, 
                      title_x=0.50)
    
    return fig
 
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)']<= payload_range[1])]
    if entered_site == 'ALL':
        title=f'<b>Payload vs. Success for All Sites. Payload Range: {payload_range} kg.</b>'
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site]
        title=f'<b>Payload vs. Success for site {entered_site}. Payload Range: {payload_range} kg.</b>'
    
    filtered_df['class_name'] = filtered_df['class'].map({0: 'Failure', 1: 'Success'})
    fig = px.scatter(filtered_df, 
                     x='Payload Mass (kg)', 
                     y='class_name',
                     color='Booster Version Category',
                     title=title)
                    #  size_max=35,
                    #  symbol_sequence=['circle', 'square', 'diamond'])

    fig.update_layout(title={'x': 0.5, 
                             'xanchor': 'center',
                             'font': {'family': 'Helvetica', 'size': 22}},
                      xaxis={'title_font': {'family': 'Helvetica', 'size': 16},
                             'tickfont': {'family': 'Helvetica', 'size': 14},
                             'range': [-100, 10_100]},
                      yaxis={'title': 'Launch Outcome',
                             'title_font': {'family': 'Helvetica', 'size': 16},
                             'tickfont': {'family': 'Helvetica', 'size': 14}})

    fig.update_traces(marker={'size': 10,
                              'line': {'width': 0.5, 'color': 'black'}})


    return fig
 
# Run the app
if __name__ == '__main__':
    app.run()