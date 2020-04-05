import dash_html_components as html
import dash_core_components as dcc
import urllib.request as ur 
import json

update = "https://api.covid19india.org/data.json"
response = ur.urlopen(update)

f = json.loads(response.read())
update_time = f["key_values"][0]["lastupdatedtime"]

def Header():
    return html.Div([
        
        get_logo(),
        get_header(),
        get_menu()
    ],className="header")

def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='../assets/header_logo.png', height='100', width='100',style={'float':'left'})
        ]),
    ])
    return logo


def get_header():
    header = html.Div([

        html.Div([
            html.H1(
                'CoVID-19 India'),
            html.Div([
                html.H3("Last Updated:"),
                html.H4(update_time,style={'marginTop':-20}), 
            ],className="update-log"),        
        ],className="hd")

    ])
    return header



def get_menu():
    menu = html.Div([
        
        dcc.Link('Indian Statistics', href='/instats/',  className="nav-link"),

        dcc.Link('Global Statistics', href='/gstats/', className="nav-link"),

        dcc.Link('Report', href='/report/',className="nav-link"),
        ],className="nav-bar")
    return menu