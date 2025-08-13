# Import required libraries
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
app.layout=html.Div(children=[html.H1('SpaceX Launch Records Dashboard'
                                      , style={'textAlign':'center'
                                               ,'color':'#503D36'
                                               ,'font-size':20
                                               , 'font-family': ['Arial', 'sans-serif']
                                              }
                                     )
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                              ,dcc.Dropdown(id='site-dropdown'
                                            ,options=[{'label': 'All Sites', 'value': 'ALL'}
                                                      ,{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}
                                                      ,{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                      ,{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
                                                      ,{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                     ]
                                            ,value='ALL'
                                            ,placeholder='Select a Launch Site'
                                            ,searchable=True
                                            ,style={'font-size':12
                                                    ,'font-family':'sans-serif'
                                                   }
                                           )
                              ,html.Br()
                              ,html.Div(dcc.Graph(id='success-pie-chart'))
                              ,html.Br()
                              ,html.P("Payload Range (Kg)")
                              ,dcc.RangeSlider(id='payload-slider'
                                               ,min=0
                                               ,max=10000
                                               ,step=1000
                                               ,marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}
                                               ,value=[0, 10000]
                                              )
                              ,html.Br()
                              ,html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                             ]
                    
                   )
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart','figure')
             ,[Input('site-dropdown','value')])
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df
                     , names='Launch Site'
                     , title='Total Successful Launches for All Sites'
                    )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df
                     , names='class'
                     , title=f'Success vs. Failed Launches for {selected_site}'
                    )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, selected_payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]
    else:
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1]) &
                                (spacex_df['Launch Site'] == selected_site)]
    fig = px.scatter(filtered_df
                     ,x='Payload Mass (kg)'
                     ,y='class'
                     ,color='Booster Version Category'
                     ,title='Correlation between Payload Mass and Launch Success'
                     ,labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'},
                     )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
