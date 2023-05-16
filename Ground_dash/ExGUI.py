import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import webbrowser
import serial

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
                dcc.Graph(id="graph1", figure={}),
            ], width=4),
            dbc.Col([
                html.H6("Data 2", className="text-center", style={"font-size": "22px", "margin-top": "40px"}),
                dcc.Graph(id="graph2", figure={}),
            ], width=4),
            dbc.Col([
                html.H6("Data 3", className="text-center", style={"font-size": "22px", "margin-top": "40px"}),
                dcc.Graph(id="graph3", figure={}),
            ], width=4),
        ], className="mb-5"),
        dbc.Row([
            dbc.Col([
                html.H6("Data 4", className="text-center mb-5", style={"font-size": "22px"}),
                dcc.Graph(id="graph4", figure={}),
            ], width=4),
            dbc.Col([
                html.H6("Data 5", className="text-center mb-5", style={"font-size": "22px"}),
                dcc.Graph(id="graph5", figure={}),
            ], width=4),
            dbc.Col([
                html.H6("Data 6", className="text-center mb-5", style={"font-size": "22px"}),
                dcc.Graph(id="graph6", figure={}),
            ], width=4),
        ])
    ])
])

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


@app.callback(Output('refresh-page', 'children'),
              [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname.startswith('/home'):
        return html.H1("")
    elif pathname.startswith('/contact'):
        return html.H1("")
    else:
        return html.H1("")


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
        webbrowser.open_new_tab("https://plotly.com/dash/")  # Replace with your desired URL for the Home button
    return "/home"


if __name__ == '__main__':
    app.run_server(debug=True)












