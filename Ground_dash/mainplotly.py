import dash
import dash_bootstrap_components as dbc
import webbrowser
import serial
import plotly.graph_objects as go
import time
import threading
import csv
import os
from plotly.subplots import make_subplots
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Set serial port
PORT_NAME = 'COM4'
BAUDRATE = '115200'

data1 = []
data2 = []
data3 = []
data4 = []
data5 = []
data6 = []

data_lock = threading.Lock()  

index = 1
while os.path.exists(f'data/data_{index}.csv'):
    index += 1
filename = f'data/data_{index}.csv'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url'),
    dbc.Navbar(
        [
            dbc.NavbarBrand(
                "DATA PLOTS",
                style={"font-size": "23px", "font-family": "Verdana, sans-serif", "margin-left": "40px"},
            ),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href="#", id="home-link", style={"font-size": "18px"})),
                    dbc.NavItem(dbc.NavLink("Contact", href="#", id="contact-link", style={"font-size": "18px"})),
                ],
                className="mr-auto",
                navbar=True,
                style={"margin-left": "4px"}
            ),
            dbc.Nav(
                dbc.NavItem(dbc.Button("Refresh", color="primary", id="refresh-button")),
                className="ml-auto",
                navbar=True,
                style={"margin-left": "auto", "margin-right": "27px"},
            ),
        ],
        color="dark",
        dark=True,
        sticky="top",
        className="navbar-dark bg-dark"
    ),
    html.Div(id='refresh-page'),
    html.Div(className='container-fluid', children=[
        dbc.Row([
            dbc.Col([
                html.H6("Data 1", className="text-center", style={"font-size": "22px", "margin-top": "40px"}),
                dcc.Graph(id="graph1", figure=go.Figure(data=go.Scatter(x=[], y=[]))),
            ], width=4),
            dbc.Col([
                html.H6("Data 2", className="text-center", style={"font-size": "22px", "margin-top": "40px"}),
                dcc.Graph(id="graph2", figure=go.Figure(data=go.Scatter(x=[], y=[]))),
            ], width=4),
            dbc.Col([
                html.H6("Data 3", className="text-center", style={"font-size": "22px", "margin-top": "40px"}),
                dcc.Graph(id="graph3", figure=go.Figure(data=go.Scatter(x=[], y=[]))),
            ], width=4),
        ], className="mb-5"),
        dbc.Row([
            dbc.Col([
                html.H6("Data 4", className="text-center mb-5", style={"font-size": "22px"}),
                dcc.Graph(id="graph4", figure=go.Figure(data=go.Scatter(x=[], y=[]))),
            ], width=4),
            dbc.Col([
                html.H6("Data 5", className="text-center mb-5", style={"font-size": "22px"}),
                dcc.Graph(id="graph5", figure=go.Figure(data=go.Scatter(x=[], y=[]))),
            ], width=4),
            dbc.Col([
                html.H6("Data 6", className="text-center mb-5", style={"font-size": "22px"}),
                dcc.Graph(id="graph6", figure=go.Figure(data=go.Scatter(x=[], y=[]))),
            ], width=4),
        ])
    ]),
    dcc.Interval(
        id='graph-update',
        interval=1000,  
        n_intervals=0
    ),
])

# Function to read data from the serial port
def read_serial_data():
    while True:
        try:
            ser = serial.Serial(PORT_NAME, BAUDRATE)  
        except serial.SerialException as e:
            print(f"Serial port opening failed: {e}")
            time.sleep(1)
            continue

        try:
            data = ser.readline().decode().strip().split(',')

            with data_lock:
                with open(filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(data)

                if len(data) == 6:
                    data1.append(float(data[0]))
                    data2.append(float(data[1]))
                    data3.append(float(data[2]))
                    data4.append(float(data[3]))
                    data5.append(float(data[4]))
                    data6.append(float(data[5]))
        except Exception as e:
            print(f"Error reading data from serial port: {e}")
            ser.close()
            time.sleep(1)
            continue

        # Close the serial port
        ser.close()
        time.sleep(1)

# Callback function to update the page content
@app.callback(Output('refresh-page', 'children'),
              [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname.startswith('/home'):
        return html.H1("")
    elif pathname.startswith('/contact'):
        return html.H1("")
    else:
        return html.H1("")

# Function Update Data
@app.callback([Output('graph1', 'figure'),
               Output('graph2', 'figure'),
               Output('graph3', 'figure'),
               Output('graph4', 'figure'),
               Output('graph5', 'figure'),
               Output('graph6', 'figure')],
              [Input('graph-update', 'n_intervals')])
def update_graphs(n_intervals):
    fig1 = go.Figure(data=go.Scatter(x=list(range(len(data1))), y=data1))
    fig2 = go.Figure(data=go.Scatter(x=list(range(len(data2))), y=data2))
    fig3 = go.Figure(data=go.Scatter(x=list(range(len(data3))), y=data3))
    fig4 = go.Figure(data=go.Scatter(x=list(range(len(data4))), y=data4))
    fig5 = go.Figure(data=go.Scatter(x=list(range(len(data5))), y=data5))
    fig6 = go.Figure(data=go.Scatter(x=list(range(len(data6))), y=data6))

    return fig1, fig2, fig3, fig4, fig5, fig6

@app.callback(Output('url', 'pathname'),
              [Input('refresh-button', 'n_clicks'),
               Input('url', 'pathname')],
              [State('url', 'pathname')])
def update_pathname(n_clicks, current_pathname, _):
    if n_clicks is None:
        return current_pathname

    if current_pathname == '/home':
        return '/home-refresh' + str(n_clicks)
    elif current_pathname == '/contact':
        return '/contact-refresh' + str(n_clicks)
    else:
        return '/refresh' + str(n_clicks)

@app.callback(Output('contact-link', 'href'),
              [Input('contact-link', 'n_clicks')])
def open_contact_link(n_clicks):
    if n_clicks is not None:
        webbrowser.open_new_tab("https://www.instagram.com/filmvyss/")
    return "/contact"

@app.callback(Output('home-link', 'href'),
              [Input('home-link', 'n_clicks')])
def open_home_link(n_clicks):
    if n_clicks is not None:
        webbrowser.open_new_tab("https://plotly.com/dash/")
    return "/home"

if __name__ == '__main__':
    serial_thread = threading.Thread(target=read_serial_data)
    serial_thread.daemon = True
    serial_thread.start()
    
    app.run_server(debug=True)
